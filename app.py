import streamlit as st
import pandas as pd
import random


def extract_and_prepare_jira_csv(uploaded_file):
    # Загружаем исходный Excel файл и извлекаем нужные столбцы B и C с 7 строки
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Извлекаем содержимое столбцов B и C, начиная с 7 строки
    df_subset = df.iloc[6:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    # Формируем итоговый CSV для импорта в Jira
    summary_list = []
    custom_link_id_list = []
    parent_link_id_list = []
    issue_type_list = []

    current_custom_link_id = None

    # Перебираем строки и заполняем итоговые списки
    for index, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']

        # Если есть значение в столбце Feature, создаём новую запись с типом "Функция"
        if pd.notna(feature):
            summary_list.append(feature)
            issue_type_list.append("Функция")
            custom_id = str(random.randint(100000, 999999))
            custom_link_id_list.append(custom_id)
            parent_link_id_list.append(None)  # Для "Функции" Parent Link ID не заполняется
            current_custom_link_id = custom_id  # Запоминаем текущий Custom Link ID для последующих строк
        # Если есть значение в столбце Details, создаём запись с типом "ФТ"
        if pd.notna(detail):
            summary_list.append(detail)
            issue_type_list.append("ФТ")
            custom_link_id_list.append(None)  # Для "ФТ" Custom Link ID не заполняется
            parent_link_id_list.append(current_custom_link_id)  # Используем последний Custom Link ID

    # Создаём итоговый DataFrame
    final_df = pd.DataFrame({
        'Summary': summary_list,
        'Custom Link ID': custom_link_id_list,
        'Parent Link ID': parent_link_id_list,
        'Issue Type': issue_type_list
    })

    return final_df


# Интерфейс Streamlit
st.title("Jira CSV Generator")

uploaded_file = st.file_uploader("Загрузите Excel файл", type=["xlsx"])

if uploaded_file:
    st.success("Файл успешно загружен!")

    # Обрабатываем файл и генерируем CSV
    result_df = extract_and_prepare_jira_csv(uploaded_file)

    # Отображаем DataFrame на экране
    st.dataframe(result_df)

    # Сохраняем результат в CSV и предоставляем ссылку для скачивания
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Скачать CSV файл",
        data=csv,
        file_name='Jira-Import.csv',
        mime='text/csv'
    )
