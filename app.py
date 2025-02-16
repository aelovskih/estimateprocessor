import streamlit as st
import pandas as pd
import random
from io import BytesIO
import openpyxl

def read_excel_data_only(file, sheet_name=0):
    """
    Читаем Excel-файл с помощью openpyxl (data_only=True),
    чтобы получить вычисленные значения формул,
    и без использования первой строки как заголовка.
    """
    file_data = file.read()
    wb = openpyxl.load_workbook(BytesIO(file_data), data_only=True)

    # Если sheet_name - число, берём лист по индексу, иначе - по имени
    if isinstance(sheet_name, int):
        sheet = wb.worksheets[sheet_name]
    else:
        sheet = wb[sheet_name]

    # Получаем все строки листа как список кортежей
    data = list(sheet.values)
    # Формируем DataFrame без заголовков (каждая строка - часть data)
    df = pd.DataFrame(data)
    return df

def find_total_cost_column_name(df):
    """
    Ищем в df столбец, в котором во второй строке (df.iloc[1]) написано "Total cost".
    Возвращаем номер столбца (int), если нашли, иначе None.
    """
    for col in df.columns:
        cell_value = df.iloc[1, col]
        if pd.notna(cell_value) and str(cell_value).strip() == "Total cost":
            return col
    return None

def process_with_epics(df):
    """Обработка с включением Epic"""
    total_cost_col = find_total_cost_column_name(df)

    # ВАЖНО: подберите нужное смещение start_row
    # чтобы первая обрабатываемая строка соответствовала ячейке B8 в Excel
    # Судя по вашим скриншотам, вероятно, это 7 (или 8)
    start_row = 7  # Попробуйте 7, если лишние строки всё ещё появляются, попробуйте 8

    # Берём со start_row до конца, только столбцы [1,2], и убираем полностью пустые строки
    df_subset = df.iloc[start_row:, [1, 2]].dropna(how='all').reset_index(drop=True)
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

        # Чтобы корректно вытянуть Total cost, берём строку в исходном df:
        original_row_index = idx + start_row

        cost_value = None
        if total_cost_col is not None and original_row_index < len(df):
            cost_value = df.iloc[original_row_index, total_cost_col]

        # Если в ячейке Feature есть значение, считаем это Эпиком
        if pd.notna(feature):
            summary_list.append(feature)
            issue_type_list.append("Epic")
            custom_id = str(random.randint(100000, 999999))
            custom_link_id_list.append(custom_id)
            parent_link_id_list.append(None)
            # Эпику Total cost не ставим (или ставим None/0)
            total_cost_list.append(None)
            current_custom_link_id = custom_id
            current_epic_name = feature

        # Если в ячейке Details есть значение, считаем это ФТ
        if pd.notna(detail):
            if current_epic_name:
                ft_summary = f"[{current_epic_name}] {detail}"
            else:
                ft_summary = detail

            summary_list.append(ft_summary)
            issue_type_list.append("ФТ")
            custom_link_id_list.append(None)
            parent_link_id_list.append(current_custom_link_id)

            # ФТ получает cost_value, если оно есть
            total_cost_list.append(cost_value if pd.notna(cost_value) else None)

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

    # Аналогичное смещение (start_row) для второго варианта
    start_row = 7  # Или 8, если нужно

    df_subset = df.iloc[start_row:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    summary_list = []
    total_cost_list = []
    current_epic_name = None

    for idx, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']

        original_row_index = idx + start_row
        cost_value = None
        if total_cost_col is not None and original_row_index < len(df):
            cost_value = df.iloc[original_row_index, total_cost_col]

        # Если нашли Feature (эпик), запоминаем, но не добавляем отдельную строчку
        if pd.notna(feature):
            current_epic_name = feature

        # Если есть Details (ФТ)
        if pd.notna(detail):
            if current_epic_name:
                summary = f"[{current_epic_name}] {detail}"
            else:
                summary = detail

            summary_list.append(summary)
            total_cost_list.append(cost_value if pd.notna(cost_value) else None)

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
        df = read_excel_data_only(uploaded_file, sheet_name=0)

        if processing_option == "Импортировать Функции как Epic's":
            result_df = process_with_epics(df)
        else:
            result_df = process_without_epics(df)

        st.dataframe(result_df)
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Скачать CSV файл",
            data=csv,
            file_name='Jira-Import.csv',
            mime='text/csv'
        )

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
