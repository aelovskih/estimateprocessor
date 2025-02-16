import streamlit as st
import pandas as pd
import random


def find_total_cost_column_name(df):
    """
    Ищем в исходном DataFrame столбец, в котором во второй строке (df.iloc[1, col])
    находится текст "Total cost". Возвращаем название столбца, если найден, иначе None.
    """
    for col in df.columns:
        cell_value = df.iloc[1][col]
        # Сравниваем по строке, учитывая, что в ячейке может быть пробелы, NaN и т.д.
        if pd.notna(cell_value) and str(cell_value).strip() == "Total cost":
            return col
    return None


def process_with_epics(uploaded_file):
    """Обработка с включением Epic"""
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Пытаемся найти столбец "Total cost" во второй строке
    total_cost_col = find_total_cost_column_name(df)

    # Загружаем нужные столбцы (B и C), пропуская первые 5 строк
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

        # Определяем "родную" строку в исходном df (т.к. мы пропустили 5 строк)
        original_row_index = idx + 5

        # Если столбец total_cost_col найден, получаем значение cost
        cost_value = None
        if total_cost_col is not None:
            cost_value = df.iloc[original_row_index][total_cost_col]

        # Обрабатываем Эпик (если Feature не пустое)
        if pd.notna(feature):
            summary_list.append(feature)
            issue_type_list.append("Epic")

            # Генерируем уникальный ID для эпика
            custom_id = str(random.randint(100000, 999999))
            custom_link_id_list.append(custom_id)
            parent_link_id_list.append(None)

            # Эпику "Total cost" не ставим (или ставим 0 / None)
            total_cost_list.append(None)

            current_custom_link_id = custom_id
            current_epic_name = feature

        # Обрабатываем ФТ (если Detail не пустое)
        if pd.notna(detail):
            # Маска для ФТ: "[Эпик] Деталь"
            if current_epic_name:
                ft_summary = f"[{current_epic_name}] {detail}"
            else:
                ft_summary = detail

            summary_list.append(ft_summary)
            issue_type_list.append("ФТ")

            # У ФТ custom_link_id не нужен, но parent_link_id указывает на эпик
            custom_link_id_list.append(None)
            parent_link_id_list.append(current_custom_link_id)

            # Для ФТ пишем cost, если он есть
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


def process_without_epics(uploaded_file):
    """Обработка без включения Epic"""
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Пытаемся найти столбец "Total cost" во второй строке
    total_cost_col = find_total_cost_column_name(df)

    # Загружаем нужные столбцы (B и C), пропуская первые 5 строк
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
        if total_cost_col is not None:
            cost_value = df.iloc[original_row_index][total_cost_col]

        # Если встречаем новый эпик — запоминаем, но НЕ создаём отдельную строку
        if pd.notna(feature):
            current_epic_name = feature

        # Если есть Details (ФТ), формируем строку с учётом текущего эпика
        if pd.notna(detail):
            if current_epic_name:
                summary = f"[{current_epic_name}] {detail}"
            else:
                summary = detail
            summary_list.append(summary)

            # Для ФТ пишем cost, если он есть
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

        if processing_option == "Импортировать Функции как Epic's":
            result_df = process_with_epics(uploaded_file)
        else:
            result_df = process_without_epics(uploaded_file)

        st.dataframe(result_df)

        # Скачивание результата
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
