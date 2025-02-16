import streamlit as st
import pandas as pd
import random
from io import BytesIO
import openpyxl

def read_excel_data_only(file, sheet_name=0):
    """
    Читаем Excel-файл с помощью openpyxl (data_only=True),
    чтобы получить вычисленные значения формул.
    
    Возвращаем DataFrame, где первая строка листа будет заголовком df.columns,
    а последующие строки — данными.
    """
    # Считываем файл как двоичный поток
    file_data = file.read()
    # Открываем workbook с data_only=True
    wb = openpyxl.load_workbook(BytesIO(file_data), data_only=True)

    # Определяем, какой лист брать (по индексу или по названию)
    if isinstance(sheet_name, int):
        sheet = wb.worksheets[sheet_name]
    else:
        sheet = wb[sheet_name]

    # Считываем все строки листа в виде списка кортежей
    data = list(sheet.values)

    # Предполагаем, что первая строка (data[0]) — это названия колонок
    # Если у вас в файле нет "правильной" строки заголовков, нужно адаптировать логику
    columns = data[0]
    rows = data[1:]

    # Создаём DataFrame
    df = pd.DataFrame(rows, columns=columns)

    return df


def find_total_cost_column_name(df):
    """
    Ищем в df столбец, в котором во второй строке (df.iloc[1, col]) написано "Total cost".
    Возвращаем название столбца (str), если нашли, иначе None.
    """
    for col in df.columns:
        cell_value = df.iloc[1][col]
        if pd.notna(cell_value) and str(cell_value).strip() == "Total cost":
            return col
    return None


def process_with_epics(df):
    """Обработка с включением Epic"""

    # Находим столбец "Total cost" во второй строке
    total_cost_col = find_total_cost_column_name(df)

    # Формируем df_subset из столбцов B, C (индексы 1, 2) после пропуска 5 строк
    # ВНИМАНИЕ: теперь в df.columns могут быть не просто 'B','C' и т.п.,
    # а реальные заголовки (или None) в зависимости от структуры файла.
    # Если исходная таблица в первых строках не имеет "правильных" названий,
    # придётся ориентироваться на индекс столбца (например, df.iloc[:, [1,2]]),
    # как мы делали раньше.
    # Предположим, что "B" и "C" — это 2-й и 3-й столбец в df (т.е. индексы 1 и 2).
    # Ниже - тот же подход, что и раньше:
    df_subset = df.iloc[5:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    summary_list = []
    custom_link_id_list = []
    parent_link_id_list = []
    issue_type_list = []
    total_cost_list = []

    current_custom_link_id = None
    current_epic_name = None

    for idx, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']

        # "Сырой" индекс в полном df, чтобы достать Total cost
        original_row_index = idx + 5

        cost_value = None
        if total_cost_col is not None and (original_row_index < len(df)):
            cost_value = df.iloc[original_row_index][total_cost_col]

        # Если есть Feature - это Эпик
        if pd.notna(feature):
            summary_list.append(feature)
            issue_type_list.append("Epic")

            custom_id = str(random.randint(100000, 999999))
            custom_link_id_list.append(custom_id)
            parent_link_id_list.append(None)

            # Эпику ставим None (или 0)
            total_cost_list.append(None)

            current_custom_link_id = custom_id
            current_epic_name = feature

        # Если есть Details - это ФТ
        if pd.notna(detail):
            if current_epic_name:
                ft_summary = f"[{current_epic_name}] {detail}"
            else:
                ft_summary = detail

            summary_list.append(ft_summary)
            issue_type_list.append("ФТ")

            custom_link_id_list.append(None)
            parent_link_id_list.append(current_custom_link_id)

            # У ФТ пишем cost
            if pd.notna(cost_value):
                total_cost_list.append(cost_value)
            else:
                total_cost_list.append(None)

    return pd.DataFrame({
        'Summary': summary_list,
        'Custom Link ID': custom_link_id_list,
        'Parent Link ID': parent_link_id_list,
        'Issue Type': issue_type_list,
        'Total cost': total_cost_list
    })


def process_without_epics(df):
    """Обработка без включения Epic"""
    total_cost_col = find_total_cost_column_name(df)

    df_subset = df.iloc[5:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    summary_list = []
    total_cost_list = []

    current_epic_name = None

    for idx, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']

        original_row_index = idx + 5
        cost_value = None
        if total_cost_col is not None and (original_row_index < len(df)):
            cost_value = df.iloc[original_row_index][total_cost_col]

        # Запоминаем новый эпик, но не создаём строку
        if pd.notna(feature):
            current_epic_name = feature

        # Если есть Details - это ФТ
        if pd.notna(detail):
            if current_epic_name:
                summary = f"[{current_epic_name}] {detail}"
            else:
                summary = detail
            summary_list.append(summary)

            # Для ФТ ставим cost
            if pd.notna(cost_value):
                total_cost_list.append(cost_value)
            else:
                total_cost_list.append(None)

    return pd.DataFrame({
        'Summary': summary_list,
        'Issue Type': ['ФТ'] * len(summary_list),
        'Total cost': total_cost_list
    })


def main():
    st.title("Jira CSV Generator")

    processing_option = st.radio(
        "Выберите вариант обработки данных:",
        ("Импортировать Функции как Epic's", "Не импортировать Эпики")
    )

    uploaded_file = st.file_uploader("Загрузите Excel файл", type=["xlsx"])

    if uploaded_file:
        st.success("Файл успешно загружен!")

        # 1. Читаем Excel-файл с "data_only=True", чтобы получить вычисленные значения.
        df = read_excel_data_only(uploaded_file, sheet_name=0)

        # 2. В зависимости от выбранного режима обрабатываем
        if processing_option == "Импортировать Функции как Epic's":
            result_df = process_with_epics(df)
        else:
            result_df = process_without_epics(df)

        # 3. Выводим результат
        st.dataframe(result_df)

        # 4. Предлагаем скачать CSV
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Скачать CSV файл",
            data=csv,
            file_name='Jira-Import.csv',
            mime='text/csv'
        )

    # Кнопка для скачивания конфиг-файла
    config_file_path = "Конфиг v2.txt"
    try:
        with open(config_file_path, 'r') as config_file:
            config_data = config_file.read()
        st.download_button(
            label="Скачать конфиг-файл для быстрого импорта",
            data=config_data,
            file_name='Jira-Import-Config.txt',
            mime='text/plain'
        )
    except FileNotFoundError:
        st.error(f"Файл {config_file_path} не найден. Убедитесь, что он загружен в репозиторий.")


if __name__ == "__main__":
    main()










# Рабочая версия от 16.02 без Total cost
# import streamlit as st
# import pandas as pd
# import random


# def process_with_epics(uploaded_file):
#     """Обработка с включением Epic"""
#     df = pd.read_excel(uploaded_file, sheet_name=0)
#     df_subset = df.iloc[5:, [1, 2]].dropna(how='all').reset_index(drop=True)
#     df_subset.columns = ['Feature', 'Details']

#     summary_list = []
#     custom_link_id_list = []
#     parent_link_id_list = []
#     issue_type_list = []

#     current_custom_link_id = None
#     current_epic_name = None  # Здесь будем хранить название текущего эпика

#     for index, row in df_subset.iterrows():
#         feature = row['Feature']
#         detail = row['Details']

#         if pd.notna(feature):
#             summary_list.append(feature)
#             issue_type_list.append("Epic")
#             custom_id = str(random.randint(100000, 999999))
#             custom_link_id_list.append(custom_id)
#             parent_link_id_list.append(None)

#             current_custom_link_id = custom_id
#             current_epic_name = feature

#         if pd.notna(detail):
#             ft_summary = f"[{current_epic_name}] {detail}" if current_epic_name else detail
#             summary_list.append(ft_summary)
#             issue_type_list.append("ФТ")
#             custom_link_id_list.append(None)
#             parent_link_id_list.append(current_custom_link_id)

#     return pd.DataFrame({
#         'Summary': summary_list,
#         'Custom Link ID': custom_link_id_list,
#         'Parent Link ID': parent_link_id_list,
#         'Issue Type': issue_type_list
#     })


# def process_without_epics(uploaded_file):
#     """Обработка без включения Epic"""
#     df = pd.read_excel(uploaded_file, sheet_name=0)
#     df_subset = df.iloc[5:, [1, 2]].dropna(how='all').reset_index(drop=True)
#     df_subset.columns = ['Feature', 'Details']

#     summary_list = []
#     current_epic_name = None  # Храним название "активного" эпика

#     for index, row in df_subset.iterrows():
#         feature = row['Feature']
#         detail = row['Details']

#         # Если в строке есть новый эпик, просто запоминаем его (но не создаём отдельную строку)
#         if pd.notna(feature):
#             current_epic_name = feature

#         # Если есть Details (ФТ), формируем строку с учётом текущего эпика
#         if pd.notna(detail):
#             if current_epic_name:
#                 summary_list.append(f"[{current_epic_name}] {detail}")
#             else:
#                 # Если эпик не задан, оставляем просто текст ФТ
#                 summary_list.append(detail)

#     # В этом варианте отдельные ID для эпиков не нужны
#     return pd.DataFrame({
#         'Summary': summary_list,
#         'Issue Type': ['ФТ'] * len(summary_list)
#     })


# def main():
#     st.title("Jira CSV Generator")

#     processing_option = st.radio(
#         "Выберите вариант обработки данных:",
#         ("Импортировать Функции как Epic's", "Не импортировать Эпики")
#     )

#     uploaded_file = st.file_uploader("Загрузите Excel файл", type=["xlsx"])

#     if uploaded_file:
#         st.success("Файл успешно загружен!")

#         if processing_option == "Импортировать Функции как Epic's":
#             result_df = process_with_epics(uploaded_file)
#         else:
#             result_df = process_without_epics(uploaded_file)

#         st.dataframe(result_df)

#         # Скачивание результата
#         csv = result_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="Скачать CSV файл",
#             data=csv,
#             file_name='Jira-Import.csv',
#             mime='text/csv'
#         )

#     # Кнопка для скачивания конфиг-файла
#     config_file_path = "Конфиг v2.txt"

#     try:
#         with open(config_file_path, 'r') as config_file:
#             config_data = config_file.read()

#         st.download_button(
#             label="Скачать конфиг-файл для быстрого импорта",
#             data=config_data,
#             file_name='Jira-Import-Config.txt',
#             mime='text/plain'
#         )
#     except FileNotFoundError:
#         st.error(f"Файл {config_file_path} не найден. Убедитесь, что он загружен в репозиторий.")


# if __name__ == "__main__":
#     main()









# Рабочая версия от 15.02 без маски
# import streamlit as st
# import pandas as pd
# import random


# def process_with_epics(uploaded_file):
#     """Обработка с включением Epic"""
#     df = pd.read_excel(uploaded_file, sheet_name=0)
#     df_subset = df.iloc[5:, [1, 2]].dropna(how='all').reset_index(drop=True)
#     df_subset.columns = ['Feature', 'Details']

#     summary_list = []
#     custom_link_id_list = []
#     parent_link_id_list = []
#     issue_type_list = []

#     current_custom_link_id = None

#     for index, row in df_subset.iterrows():
#         feature = row['Feature']
#         detail = row['Details']

#         if pd.notna(feature):
#             summary_list.append(feature)
#             issue_type_list.append("Epic")
#             custom_id = str(random.randint(100000, 999999))
#             custom_link_id_list.append(custom_id)
#             parent_link_id_list.append(None)
#             current_custom_link_id = custom_id

#         if pd.notna(detail):
#             summary_list.append(detail)
#             issue_type_list.append("ФТ")
#             custom_link_id_list.append(None)
#             parent_link_id_list.append(current_custom_link_id)

#     return pd.DataFrame({
#         'Summary': summary_list,
#         'Custom Link ID': custom_link_id_list,
#         'Parent Link ID': parent_link_id_list,
#         'Issue Type': issue_type_list
#     })


# def process_without_epics(uploaded_file):
#     """Обработка без включения Epic"""
#     df = pd.read_excel(uploaded_file, sheet_name=0)
#     df_subset = df.iloc[5:, [1, 2]].dropna(how='all').reset_index(drop=True)
#     df_subset.columns = ['Feature', 'Details']

#     summary_list = []

#     for index, row in df_subset.iterrows():
#         feature = row['Feature']
#         detail = row['Details']

#         if pd.notna(detail):
#             # Добавляем "[Feature] Details" только если Feature заполнен
#             if pd.notna(feature):
#                 summary = f"[{feature}] {detail}"
#             else:
#                 summary = detail  # Если Feature пустой, оставляем только Details
#             summary_list.append(summary)

#     return pd.DataFrame({
#         'Summary': summary_list,
#         'Issue Type': ['ФТ'] * len(summary_list)  # Все задачи — тип ФТ
#     })


# # Интерфейс Streamlit
# st.title("Jira CSV Generator")

# processing_option = st.radio(
#     "Выберите вариант обработки данных:",
#     ("Импортировать Функции как Epic's", "Не импортировать Эпики")
# )

# uploaded_file = st.file_uploader("Загрузите Excel файл", type=["xlsx"])

# if uploaded_file:
#     st.success("Файл успешно загружен!")

#     if processing_option == "Импортировать Функции как Epic's":
#         result_df = process_with_epics(uploaded_file)
#     else:
#         result_df = process_without_epics(uploaded_file)

#     st.dataframe(result_df)

#     # Скачивание результата
#     csv = result_df.to_csv(index=False).encode('utf-8')
#     st.download_button(
#         label="Скачать CSV файл",
#         data=csv,
#         file_name='Jira-Import.csv',
#         mime='text/csv'
#     )

# # Кнопка для скачивания конфиг-файла
# config_file_path = "Конфиг v2.txt"

# try:
#     with open(config_file_path, 'r') as config_file:
#         config_data = config_file.read()

#     st.download_button(
#         label="Скачать конфиг-файл для быстрого импорта",
#         data=config_data,
#         file_name='Jira-Import-Config.txt',
#         mime='text/plain'
#     )
# except FileNotFoundError:
#     st.error(f"Файл {config_file_path} не найден. Убедитесь, что он загружен в репозиторий.")
