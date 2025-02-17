import streamlit as st
import pandas as pd
import random
from io import BytesIO
import openpyxl

#############################
# 1. Список допустимых грейдов
#############################
allowed_grades = [
    "Продуктовая аналитика стажер",
    "UX-аналитик junior",
    "UX-аналитик middle -",
    "UX-аналитик middle",
    "UX-аналитик senior",
    "Web/mobile-аналитик junior",
    "Web/mobile-аналитик middle -",
    "Web/mobile-аналитик middle",
    "Web/mobile-аналитик middle +",
    "Web/mobile-аналитик senior",
    "Web/mobile-аналитик TL",
    "BI/data-аналитик junior",
    "BI/data-аналитик middle",
    "BI/data-аналитик middle +",
    "BI/data-аналитик senior",
    "Product manager junior",
    "Product manager middle",
    "Product manager middle +",
    "Product manager Senior",
    "Web/mobile-analyst middle",
    "Web/mobile-analyst senior",
    "Дизайнер стажер",
    "Дизайнер junior-",
    "Дизайнер junior",
    "Дизайнер junior+",
    "Дизайнер middle-",
    "Дизайнер middle",
    "Дизайнер middle+",
    "Дизайнер senior",
    "Дизайнер senior+",
    "Art Director",
    "Web middle",
    "Web senior",
    "Системный аналитик Стажер",
    "Системный аналитик junior-",
    "Системный аналитик junior",
    "Системный аналитик junior+",
    "Системный аналитик middle-",
    "Системный аналитик middle",
    "Системный аналитик middle+",
    "Системный аналитик senior",
    "Системный аналитик senior+",
    "Системный аналитик lead",
    "Проектировщик стажер",
    "Проектировщик junior",
    "Проектировщик middle",
    "Проектировщик middle+",
    "Проектировщик senior",
    "Проектировщик senior+",
    "Проектировщик lead",
    "System analyst middle",
    "System analyst senior",
    "SEO",
    "tech.writer",
    "UX writer",
    "PM стажер",
    "PM intern",
    "PM junior",
    "PM junior+",
    "PM middle",
    "PM middle+",
    "PM senior",
    "PM senior+",
    "GH",
    "PMO",
    "Bitrix junior",
    "Bitrix junior+",
    "Bitrix middle-",
    "Bitrix middle",
    "Bitrix middle+",
    "Bitrix senior-",
    "Bitrix senior",
    "Bitrix senior+",
    "Bitrix teamlead -",
    "Bitrix teamlead",
    "Bitrix teamlead +",
    "Bitrix teamlead grouphead -",
    "Bitrix teamlead grouphead",
    "Bitrix teamlead grouphead +",
    "Bitrix middle",
    "Bitrix senior",
    "Разработка стажер",
    "Framework junior",
    "Framework junior+",
    "Framework middle-",
    "Framework middle",
    "Framework middle+",
    "Framework senior-",
    "Framework senior",
    "Framework senior+",
    "Framework teamlead -",
    "Framework teamlead",
    "Framework teamlead +",
    "Framework teamlead grouphead -",
    "Framework teamlead grouphead",
    "Framework teamlead grouphead +",
    "Framework middle",
    "Framework senior",
    "QA junior-",
    "QA junior",
    "QA junior +",
    "QA middle-",
    "QA middle",
    "QA middle+",
    "QA senior -",
    "QA senior",
    "QA Teamlead",
    "AQA junior-",
    "AQA junior",
    "AQA junior +",
    "AQA middle-",
    "AQA middle",
    "AQA middle+",
    "AQA senior -",
    "AQA senior",
    "AQA teamlead",
    "QA middle",
    "QA senior",
    "QA AT Middle",
    "QA AT Senior",
    "Front-end junior",
    "Front-end junior +",
    "Front-end middle -",
    "Front-end middle",
    "Front-end middle +",
    "Front-end senior -",
    "Front-end senior",
    "Front-end senior +",
    "Front-end teamlead",
    "NodeJS junior",
    "NodeJS junior +",
    "NodeJS middle -",
    "NodeJS middle",
    "NodeJS middle +",
    "NodeJS senior -",
    "NodeJS senior",
    "NodeJS senior +",
    "NodeJS teamlead",
    "Front-end html/css middle -",
    "Front-end html/css middle",
    "Front-end html/css middle +",
    "Front-end middle",
    "Front-end senior",
    "NodeJS middle",
    "NodeJS senior",
    "Front-end html/css middle",
    "Mobile Dev Junior-",
    "Mobile Dev Junior",
    "Mobile Dev Junior+",
    "Mobile Dev Middle-",
    "Mobile Dev Middle",
    "Mobile Dev Middle+",
    "Mobile Dev Senior-",
    "Mobile Dev Senior",
    "Mobile Dev Senior+",
    "Mobile Dev Teamlead",
    "Mobile dev middle",
    "Mobile dev senior",
    "Python junior",
    "Python middle-",
    "Python middle",
    "Python middle+",
    "Python senior-",
    "Python senior",
    "Python senior+",
    "Python teamlead",
    "Golang junior",
    "Golang middle-",
    "Golang middle",
    "Golang middle+",
    "Golang senior-",
    "Golang senior",
    "Golang senior+",
    "Golang teamlead",
    "Python middle",
    "Python senior",
    "Golang middle",
    "Golang senior",
    "Devops junior",
    "Devops middle-",
    "Devops middle",
    "Devops middle+",
    "Devops senior-",
    "Devops senior",
    "Devops senior+",
    "Devops teamlead",
    "Devops middle",
    "Devops senior",
    "Java middle",
    "Java senior",
    ".NET",
    ".NET Senior",
    "Security Specialist",
    "Lead Programmer Researcher / AI",
    "Programmer researcher / AI",
    "Senior data analyst / AI",
    "Middle data analyst / AI",
    "Junior data analyst / AI",
    "PM / AI",
    "Teamlead / AI",
    "Product analyst / AI",
    "Solution Architect consultant / AI",
    "Pr-manager junior",
    "Pr-manager middle",
    "Pr-manager senior",
    "DevRel junior",
    "DevRel middle",
    "DevRel senior",
    "Copywriter middle",
    "Copywriter senior",
    "Photographer/Videographer",
    "Copywriter middle",
    "Copywriter senior",
    "Content Manager",
    # ... если что-то вдруг нужно добавить, можно дополнять этот список
]

#############################
# 2. Чтение Excel (с формулами как значениями)
#############################
def read_excel_data_only(file, sheet_name=0):
    file_data = file.read()
    wb = openpyxl.load_workbook(BytesIO(file_data), data_only=True)
    if isinstance(sheet_name, int):
        sheet = wb.worksheets[sheet_name]
    else:
        sheet = wb[sheet_name]

    data = list(sheet.values)
    df = pd.DataFrame(data)
    return df

#############################
# 3. Функция для проверки грейдов
#############################
def check_grades(df, allowed_grades):
    """
    Проверяем в 3-й строке (индекс 2) ячейки на значения "Inside" или "Outside".
    Если находим такие ячейки, значит во 2-й строке (индекс 1) лежит грейд.
    Сравниваем грейд со списком allowed_grades.
    Если находим незнакомый грейд, собираем в множество unknown_grades.
    Возвращаем множество unknown_grades (или пустое множество).
    """
    unknown_grades = set()

    # Перебираем все столбцы df
    for col in df.columns:
        # Смотрим, что написано в 3-й строке (индекс 2)
        if len(df) > 2:  # чтобы не выйти за границы, если таблица меньше 3 строк
            third_row_value = df.iloc[2, col]
            if pd.notna(third_row_value):
                text = str(third_row_value).strip().lower()
                # Если "Inside" или "Outside", значит в строке выше (index=1) лежит грейд
                if text in ["inside", "outside"]:
                    # Читаем грейд
                    grade_val = df.iloc[1, col]
                    if pd.notna(grade_val):
                        grade_str = str(grade_val).strip()
                        # Сравниваем с списком
                        if grade_str not in allowed_grades:
                            unknown_grades.add(grade_str)

    return unknown_grades

#############################
# 4. Остальные функции (пример)
#############################
def find_total_cost_column_name(df):
    for col in df.columns:
        cell_value = df.iloc[1, col]
        if pd.notna(cell_value) and str(cell_value).strip() == "Total cost":
            return col
    return None

def process_with_epics(df):
    total_cost_col = find_total_cost_column_name(df)
    start_row = 7  # Примерное смещение, подберите под вашу структуру

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
        original_row_index = idx + start_row

        cost_value = None
        if total_cost_col is not None and original_row_index < len(df):
            cost_value = df.iloc[original_row_index, total_cost_col]

        if pd.notna(feature):
            summary_list.append(feature)
            issue_type_list.append("Epic")
            custom_id = str(random.randint(100000, 999999))
            custom_link_id_list.append(custom_id)
            parent_link_id_list.append(None)
            total_cost_list.append(None)
            current_custom_link_id = custom_id
            current_epic_name = feature

        if pd.notna(detail):
            if current_epic_name:
                ft_summary = f"[{current_epic_name}] {detail}"
            else:
                ft_summary = detail

            summary_list.append(ft_summary)
            issue_type_list.append("ФТ")
            custom_link_id_list.append(None)
            parent_link_id_list.append(current_custom_link_id)
            total_cost_list.append(cost_value if pd.notna(cost_value) else None)

    return pd.DataFrame({
        'Summary': summary_list,
        'Custom Link ID': custom_link_id_list,
        'Parent Link ID': parent_link_id_list,
        'Issue Type': issue_type_list,
        'Total cost': total_cost_list
    })

def process_without_epics(df):
    total_cost_col = find_total_cost_column_name(df)
    start_row = 7

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

        if pd.notna(feature):
            current_epic_name = feature

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

#############################
# 5. Основной поток (Streamlit)
#############################
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

        # Сначала проверяем грейды
        unknown_grades = check_grades(df, allowed_grades)
        if unknown_grades:
            st.warning(
                "Внимание! В смете присутствуют неизвестные грейды: "
                + ", ".join(unknown_grades)
            )

        # Затем продолжаем обычную обработку
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










# import streamlit as st
# import pandas as pd
# import random
# from io import BytesIO
# import openpyxl

# def read_excel_data_only(file, sheet_name=0):
#     """
#     Читаем Excel-файл с помощью openpyxl (data_only=True),
#     чтобы получить вычисленные значения формул,
#     и без использования первой строки как заголовка.
#     """
#     file_data = file.read()
#     wb = openpyxl.load_workbook(BytesIO(file_data), data_only=True)

#     # Если sheet_name - число, берём лист по индексу, иначе - по имени
#     if isinstance(sheet_name, int):
#         sheet = wb.worksheets[sheet_name]
#     else:
#         sheet = wb[sheet_name]

#     # Получаем все строки листа как список кортежей
#     data = list(sheet.values)
#     # Формируем DataFrame без заголовков (каждая строка - часть data)
#     df = pd.DataFrame(data)
#     return df

# def find_total_cost_column_name(df):
#     """
#     Ищем в df столбец, в котором во второй строке (df.iloc[1]) написано "Total cost".
#     Возвращаем номер столбца (int), если нашли, иначе None.
#     """
#     for col in df.columns:
#         cell_value = df.iloc[1, col]
#         if pd.notna(cell_value) and str(cell_value).strip() == "Total cost":
#             return col
#     return None

# def process_with_epics(df):
#     """Обработка с включением Epic"""
#     total_cost_col = find_total_cost_column_name(df)

#     # ВАЖНО: подберите нужное смещение start_row
#     # чтобы первая обрабатываемая строка соответствовала ячейке B8 в Excel
#     # Судя по вашим скриншотам, вероятно, это 7 (или 8)
#     start_row = 7  # Попробуйте 7, если лишние строки всё ещё появляются, попробуйте 8

#     # Берём со start_row до конца, только столбцы [1,2], и убираем полностью пустые строки
#     df_subset = df.iloc[start_row:, [1, 2]].dropna(how='all').reset_index(drop=True)
#     df_subset.columns = ['Feature', 'Details']

#     summary_list = []
#     custom_link_id_list = []
#     parent_link_id_list = []
#     issue_type_list = []
#     total_cost_list = []

#     current_custom_link_id = None
#     current_epic_name = None

#     for idx, row in df_subset.iterrows():
#         feature = row['Feature']
#         detail = row['Details']

#         # Чтобы корректно вытянуть Total cost, берём строку в исходном df:
#         original_row_index = idx + start_row

#         cost_value = None
#         if total_cost_col is not None and original_row_index < len(df):
#             cost_value = df.iloc[original_row_index, total_cost_col]

#         # Если в ячейке Feature есть значение, считаем это Эпиком
#         if pd.notna(feature):
#             summary_list.append(feature)
#             issue_type_list.append("Epic")
#             custom_id = str(random.randint(100000, 999999))
#             custom_link_id_list.append(custom_id)
#             parent_link_id_list.append(None)
#             # Эпику Total cost не ставим (или ставим None/0)
#             total_cost_list.append(None)
#             current_custom_link_id = custom_id
#             current_epic_name = feature

#         # Если в ячейке Details есть значение, считаем это ФТ
#         if pd.notna(detail):
#             if current_epic_name:
#                 ft_summary = f"[{current_epic_name}] {detail}"
#             else:
#                 ft_summary = detail

#             summary_list.append(ft_summary)
#             issue_type_list.append("ФТ")
#             custom_link_id_list.append(None)
#             parent_link_id_list.append(current_custom_link_id)

#             # ФТ получает cost_value, если оно есть
#             total_cost_list.append(cost_value if pd.notna(cost_value) else None)

#     return pd.DataFrame({
#         'Summary': summary_list,
#         'Custom Link ID': custom_link_id_list,
#         'Parent Link ID': parent_link_id_list,
#         'Issue Type': issue_type_list,
#         'Total cost': total_cost_list
#     })

# def process_without_epics(df):
#     """Обработка без включения Epic"""
#     total_cost_col = find_total_cost_column_name(df)

#     # Аналогичное смещение (start_row) для второго варианта
#     start_row = 7  # Или 8, если нужно

#     df_subset = df.iloc[start_row:, [1, 2]].dropna(how='all').reset_index(drop=True)
#     df_subset.columns = ['Feature', 'Details']

#     summary_list = []
#     total_cost_list = []
#     current_epic_name = None

#     for idx, row in df_subset.iterrows():
#         feature = row['Feature']
#         detail = row['Details']

#         original_row_index = idx + start_row
#         cost_value = None
#         if total_cost_col is not None and original_row_index < len(df):
#             cost_value = df.iloc[original_row_index, total_cost_col]

#         # Если нашли Feature (эпик), запоминаем, но не добавляем отдельную строчку
#         if pd.notna(feature):
#             current_epic_name = feature

#         # Если есть Details (ФТ)
#         if pd.notna(detail):
#             if current_epic_name:
#                 summary = f"[{current_epic_name}] {detail}"
#             else:
#                 summary = detail

#             summary_list.append(summary)
#             total_cost_list.append(cost_value if pd.notna(cost_value) else None)

#     return pd.DataFrame({
#         'Summary': summary_list,
#         'Issue Type': ['ФТ'] * len(summary_list),
#         'Total cost': total_cost_list
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
#         df = read_excel_data_only(uploaded_file, sheet_name=0)

#         if processing_option == "Импортировать Функции как Epic's":
#             result_df = process_with_epics(df)
#         else:
#             result_df = process_without_epics(df)

#         st.dataframe(result_df)
#         csv = result_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="Скачать CSV файл",
#             data=csv,
#             file_name='Jira-Import.csv',
#             mime='text/csv'
#         )

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
