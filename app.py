import streamlit as st
import pandas as pd
import random


def process_with_epics(uploaded_file):
    """Обработка с включением Epic"""
    df = pd.read_excel(uploaded_file, sheet_name=0)
    # Пропускаем первые 5 строк и берем только столбцы B, C (индексы 1 и 2)
    df_subset = df.iloc[5:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    summary_list = []
    custom_link_id_list = []
    parent_link_id_list = []
    issue_type_list = []

    current_custom_link_id = None
    current_epic_name = None  # Здесь будем хранить название последнего эпика

    for index, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']

        # Если в строке есть значение в столбце Feature — это наш эпик
        if pd.notna(feature):
            summary_list.append(feature)
            issue_type_list.append("Epic")

            # Генерируем уникальный ID для эпика
            custom_id = str(random.randint(100000, 999999))
            custom_link_id_list.append(custom_id)
            parent_link_id_list.append(None)

            # Запоминаем ID и название эпика
            current_custom_link_id = custom_id
            current_epic_name = feature

        # Если есть значение в столбце Details — это ФТ
        if pd.notna(detail):
            # Маска: "[Эпик] ФТ"
            ft_summary = f"[{current_epic_name}] {detail}"

            summary_list.append(ft_summary)
            issue_type_list.append("ФТ")

            # Для ФТ custom_link_id не нужен, но parent_link_id должен указывать на эпик
            custom_link_id_list.append(None)
            parent_link_id_list.append(current_custom_link_id)

    # Формируем итоговый DataFrame
    return pd.DataFrame({
        'Summary': summary_list,
        'Custom Link ID': custom_link_id_list,
        'Parent Link ID': parent_link_id_list,
        'Issue Type': issue_type_list
    })


def process_without_epics(uploaded_file):
    """Обработка без включения Epic"""
    df = pd.read_excel(uploaded_file, sheet_name=0)
    df_subset = df.iloc[5:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    summary_list = []

    for index, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']

        if pd.notna(detail):
            # Добавляем "[Feature] Details" только если Feature заполнен
            if pd.notna(feature):
                summary = f"[{feature}] {detail}"
            else:
                summary = detail  # Если Feature пустой, оставляем только Details
            summary_list.append(summary)

    return pd.DataFrame({
        'Summary': summary_list,
        'Issue Type': ['ФТ'] * len(summary_list)  # Все задачи — тип ФТ
    })


# Интерфейс Streamlit
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









# Рабочая версия от 16.02
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
