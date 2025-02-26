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
# 3. Проверка грейдов
#############################
def check_grades(df, allowed_grades):
    unknown_grades = set()
    for col in df.columns:
        if len(df) > 2:
            third_row_value = df.iloc[2, col]
            if pd.notna(third_row_value):
                text = str(third_row_value).strip().lower()
                if text in ["inside", "outside"]:
                    grade_val = df.iloc[1, col]
                    if pd.notna(grade_val):
                        grade_str = str(grade_val).strip()
                        if grade_str not in allowed_grades:
                            unknown_grades.add(grade_str)
    return unknown_grades

#############################
# 4. Поиск столбца "Total cost"
#############################
def find_total_cost_column_name(df):
    for col in df.columns:
        cell_value = df.iloc[1, col]
        if pd.notna(cell_value) and str(cell_value).strip() == "Total cost":
            return col
    return None

#############################
# 5. Функция для обработки имени эпика
#############################
def process_function_name(epic_name):
    # Заменяем пробелы на нижние подчёркивания
    return "_".join(epic_name.split())

#############################
# 6. Жёстко берём столбцы F..Y как "оценочные"
#############################
def get_time_estimate_columns(df):
    """
    Возвращает список кортежей (grade_name, col_index) для столбцов F..Y (индексы 5..24),
    где во 2-й строке (index=1) указано название грейда,
    а в 3-й строке (index=2) написано 'Inside' или 'Outside'.
    """
    grade_cols = []
    for col in range(5, 25):  # F..Y
        if col < len(df.columns):
            third_row_value = df.iloc[2, col]
            if pd.notna(third_row_value):
                text = str(third_row_value).strip().lower()
                if text in ["inside", "outside"]:
                    grade_val = df.iloc[1, col]
                    if pd.notna(grade_val):
                        grade_str = str(grade_val).strip()
                        grade_cols.append((grade_str, col))
    return grade_cols

#############################
# 7. Обработка "с эпиками"
#############################
def process_with_epics(df):
    total_cost_col = find_total_cost_column_name(df)
    grade_cols = get_time_estimate_columns(df)
    start_row = 7  # Подберите под структуру

    # Подготовка df_subset
    df_subset = df.iloc[start_row:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    # Основные списки
    summary_list = []
    custom_link_id_list = []
    parent_link_id_list = []
    issue_type_list = []
    total_cost_list = []
    function_name_list = []

    # Списки для грейдов
    grade_values = {grade_name: [] for (grade_name, _) in grade_cols}

    current_custom_link_id = None
    current_function_name = None

    # -- Основной цикл --
    for idx, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']
        original_row_index = idx + start_row

        # Смотрим на Total cost
        cost_value = None
        if total_cost_col is not None and original_row_index < len(df):
            cost_value = df.iloc[original_row_index, total_cost_col]

        # Проверяем, является ли строка эпиком
        if pd.notna(feature) and str(feature).strip() != "":
            # Создаём строку для эпика
            custom_id = str(random.randint(100000, 999999))
            processed_fn = process_function_name(str(feature))

            summary_list.append(feature)  # Summary = сам эпик
            issue_type_list.append("Epic")
            custom_link_id_list.append(custom_id)
            parent_link_id_list.append(None)
            total_cost_list.append(None)  # у эпика нет total cost
            function_name_list.append(processed_fn)

            current_custom_link_id = custom_id
            current_function_name = processed_fn

            # Времязатраты для эпика = None
            for gname in grade_values:
                grade_values[gname].append(None)

        # Проверяем, является ли строка ФТ
        if pd.notna(detail) and str(detail).strip() != "":
            # Создаём строку для ФТ
            summary_list.append(detail)  # Summary = только столбец C
            issue_type_list.append("ФТ")
            custom_link_id_list.append(None)
            parent_link_id_list.append(current_custom_link_id)
            total_cost_list.append(cost_value if pd.notna(cost_value) else None)
            function_name_list.append(current_function_name if current_function_name else None)

            # Времязатраты для ФТ
            for (grade_name, col_index) in grade_cols:
                if original_row_index < len(df):
                    val = df.iloc[original_row_index, col_index]
                    if pd.notna(val) and float(val) != 0.0:
                        grade_values[grade_name].append(val)
                    else:
                        grade_values[grade_name].append(None)

    # -- Формируем итоговый DataFrame --
    result_df = pd.DataFrame({
        'Summary': summary_list,
        'Custom Link ID': custom_link_id_list,
        'Parent Link ID': parent_link_id_list,
        'Issue Type': issue_type_list,
        'Total cost': total_cost_list,
        'Function name': function_name_list
    })

    # -- Отладка: выводим длины списков в Streamlit --
    st.write("### Отладочная информация (с эпиками)")
    st.write(f"Итоговое количество строк в result_df: {len(result_df)}")
    st.write(f"Количество строк в summary_list: {len(summary_list)}")
    for grade_name, _ in grade_cols:
        st.write(f"Грейд '{grade_name}': {len(grade_values[grade_name])} записей")

    # -- Добавляем столбцы по грейдам --
    for (grade_name, _) in grade_cols:
        # Если выяснится, что длина не совпадает, вы это увидите в отладке
        result_df[grade_name] = grade_values[grade_name]

    return result_df

#############################
# 8. Обработка "без эпиков"
#############################
def process_without_epics(df):
    total_cost_col = find_total_cost_column_name(df)
    grade_cols = get_time_estimate_columns(df)
    start_row = 7

    df_subset = df.iloc[start_row:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    summary_list = []
    total_cost_list = []
    function_name_list = []
    issue_type_list = []

    grade_values = {grade_name: [] for (grade_name, _) in grade_cols}

    current_function_name = None

    for idx, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']
        original_row_index = idx + start_row

        cost_value = None
        if total_cost_col is not None and original_row_index < len(df):
            cost_value = df.iloc[original_row_index, total_cost_col]

        # Если есть Feature (эпик), запоминаем, но не создаём отдельную строку
        if pd.notna(feature) and str(feature).strip() != "":
            current_function_name = process_function_name(str(feature))

        # Если есть Details (ФТ)
        if pd.notna(detail) and str(detail).strip() != "":
            summary_list.append(detail)
            total_cost_list.append(cost_value if pd.notna(cost_value) else None)
            function_name_list.append(current_function_name if current_function_name else None)
            issue_type_list.append("ФТ")

            # Для каждого грейда
            for (grade_name, col_index) in grade_cols:
                if original_row_index < len(df):
                    val = df.iloc[original_row_index, col_index]
                    if pd.notna(val) and float(val) != 0.0:
                        grade_values[grade_name].append(val)
                    else:
                        grade_values[grade_name].append(None)
        else:
            # Если строка вообще не содержит ФТ (detail), 
            # то не добавляем строку, следовательно, не добавляем в grade_values
            # никаких значений.
            pass

    result_df = pd.DataFrame({
        'Summary': summary_list,
        'Issue Type': issue_type_list,
        'Total cost': total_cost_list,
        'Function name': function_name_list
    })

    # -- Отладка: выводим длины списков в Streamlit --
    st.write("### Отладочная информация (без эпиков)")
    st.write(f"Итоговое количество строк в result_df: {len(result_df)}")
    st.write(f"Количество строк в summary_list: {len(summary_list)}")
    for grade_name, _ in grade_cols:
        st.write(f"Грейд '{grade_name}': {len(grade_values[grade_name])} записей")

    # Добавляем столбцы по грейдам
    for (grade_name, _) in grade_cols:
        result_df[grade_name] = grade_values[grade_name]

    return result_df

#############################
# 9. Основной поток (Streamlit)
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

        # Проверяем грейды
        unknown_grades = check_grades(df, allowed_grades)
        if unknown_grades:
            st.warning(
                "Внимание! В смете присутствуют неизвестные грейды: " + ", ".join(unknown_grades)
            )

        if processing_option == "Импортировать Функции как Epic's":
            result_df = process_with_epics(df)
        else:
            result_df = process_without_epics(df)

        # Показываем DataFrame
        st.dataframe(result_df)

        # Скачивание CSV
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








# ВЕРСИЯ 0.3

# import streamlit as st
# import pandas as pd
# import random
# from io import BytesIO
# import openpyxl

# #############################
# # 1. Список допустимых грейдов (оставляем для проверки)
# #############################
# allowed_grades = [
#     "Продуктовая аналитика стажер",
#     "UX-аналитик junior",
#     "UX-аналитик middle -",
#     "UX-аналитик middle",
#     "UX-аналитик senior",
#     "Web/mobile-аналитик junior",
#     "Web/mobile-аналитик middle -",
#     "Web/mobile-аналитик middle",
#     "Web/mobile-аналитик middle +",
#     "Web/mobile-аналитик senior",
#     "Web/mobile-аналитик TL",
#     "BI/data-аналитик junior",
#     "BI/data-аналитик middle",
#     "BI/data-аналитик middle +",
#     "BI/data-аналитик senior",
#     "Product manager junior",
#     "Product manager middle",
#     "Product manager middle +",
#     "Product manager Senior",
#     "Web/mobile-analyst middle",
#     "Web/mobile-analyst senior",
#     "Дизайнер стажер",
#     "Дизайнер junior-",
#     "Дизайнер junior",
#     "Дизайнер junior+",
#     "Дизайнер middle-",
#     "Дизайнер middle",
#     "Дизайнер middle+",
#     "Дизайнер senior",
#     "Дизайнер senior+",
#     "Art Director",
#     "Web middle",
#     "Web senior",
#     "Системный аналитик Стажер",
#     "Системный аналитик junior-",
#     "Системный аналитик junior",
#     "Системный аналитик junior+",
#     "Системный аналитик middle-",
#     "Системный аналитик middle",
#     "Системный аналитик middle+",
#     "Системный аналитик senior",
#     "Системный аналитик senior+",
#     "Системный аналитик lead",
#     "Проектировщик стажер",
#     "Проектировщик junior",
#     "Проектировщик middle",
#     "Проектировщик middle+",
#     "Проектировщик senior",
#     "Проектировщик senior+",
#     "Проектировщик lead",
#     "System analyst middle",
#     "System analyst senior",
#     "SEO",
#     "tech.writer",
#     "UX writer",
#     "PM стажер",
#     "PM intern",
#     "PM junior",
#     "PM junior+",
#     "PM middle",
#     "PM middle+",
#     "PM senior",
#     "PM senior+",
#     "GH",
#     "PMO",
#     "Bitrix junior",
#     "Bitrix junior+",
#     "Bitrix middle-",
#     "Bitrix middle",
#     "Bitrix middle+",
#     "Bitrix senior-",
#     "Bitrix senior",
#     "Bitrix senior+",
#     "Bitrix teamlead -",
#     "Bitrix teamlead",
#     "Bitrix teamlead +",
#     "Bitrix teamlead grouphead -",
#     "Bitrix teamlead grouphead",
#     "Bitrix teamlead grouphead +",
#     "Bitrix middle",
#     "Bitrix senior",
#     "Разработка стажер",
#     "Framework junior",
#     "Framework junior+",
#     "Framework middle-",
#     "Framework middle",
#     "Framework middle+",
#     "Framework senior-",
#     "Framework senior",
#     "Framework senior+",
#     "Framework teamlead -",
#     "Framework teamlead",
#     "Framework teamlead +",
#     "Framework teamlead grouphead -",
#     "Framework teamlead grouphead",
#     "Framework teamlead grouphead +",
#     "Framework middle",
#     "Framework senior",
#     "QA junior-",
#     "QA junior",
#     "QA junior +",
#     "QA middle-",
#     "QA middle",
#     "QA middle+",
#     "QA senior -",
#     "QA senior",
#     "QA Teamlead",
#     "AQA junior-",
#     "AQA junior",
#     "AQA junior +",
#     "AQA middle-",
#     "AQA middle",
#     "AQA middle+",
#     "AQA senior -",
#     "AQA senior",
#     "AQA teamlead",
#     "QA middle",
#     "QA senior",
#     "QA AT Middle",
#     "QA AT Senior",
#     "Front-end junior",
#     "Front-end junior +",
#     "Front-end middle -",
#     "Front-end middle",
#     "Front-end middle +",
#     "Front-end senior -",
#     "Front-end senior",
#     "Front-end senior +",
#     "Front-end teamlead",
#     "NodeJS junior",
#     "NodeJS junior +",
#     "NodeJS middle -",
#     "NodeJS middle",
#     "NodeJS middle +",
#     "NodeJS senior -",
#     "NodeJS senior",
#     "NodeJS senior +",
#     "NodeJS teamlead",
#     "Front-end html/css middle -",
#     "Front-end html/css middle",
#     "Front-end html/css middle +",
#     "Front-end middle",
#     "Front-end senior",
#     "NodeJS middle",
#     "NodeJS senior",
#     "Front-end html/css middle",
#     "Mobile Dev Junior-",
#     "Mobile Dev Junior",
#     "Mobile Dev Junior+",
#     "Mobile Dev Middle-",
#     "Mobile Dev Middle",
#     "Mobile Dev Middle+",
#     "Mobile Dev Senior-",
#     "Mobile Dev Senior",
#     "Mobile Dev Senior+",
#     "Mobile Dev Teamlead",
#     "Mobile dev middle",
#     "Mobile dev senior",
#     "Python junior",
#     "Python middle-",
#     "Python middle",
#     "Python middle+",
#     "Python senior-",
#     "Python senior",
#     "Python senior+",
#     "Python teamlead",
#     "Golang junior",
#     "Golang middle-",
#     "Golang middle",
#     "Golang middle+",
#     "Golang senior-",
#     "Golang senior",
#     "Golang senior+",
#     "Golang teamlead",
#     "Python middle",
#     "Python senior",
#     "Golang middle",
#     "Golang senior",
#     "Devops junior",
#     "Devops middle-",
#     "Devops middle",
#     "Devops middle+",
#     "Devops senior-",
#     "Devops senior",
#     "Devops senior+",
#     "Devops teamlead",
#     "Devops middle",
#     "Devops senior",
#     "Java middle",
#     "Java senior",
#     ".NET",
#     ".NET Senior",
#     "Security Specialist",
#     "Lead Programmer Researcher / AI",
#     "Programmer researcher / AI",
#     "Senior data analyst / AI",
#     "Middle data analyst / AI",
#     "Junior data analyst / AI",
#     "PM / AI",
#     "Teamlead / AI",
#     "Product analyst / AI",
#     "Solution Architect consultant / AI",
#     "Pr-manager junior",
#     "Pr-manager middle",
#     "Pr-manager senior",
#     "DevRel junior",
#     "DevRel middle",
#     "DevRel senior",
#     "Copywriter middle",
#     "Copywriter senior",
#     "Photographer/Videographer",
#     "Copywriter middle",
#     "Copywriter senior",
#     "Content Manager",
# ]

# #############################
# # 2. Чтение Excel (с формулами как значениями)
# #############################
# def read_excel_data_only(file, sheet_name=0):
#     file_data = file.read()
#     wb = openpyxl.load_workbook(BytesIO(file_data), data_only=True)
#     if isinstance(sheet_name, int):
#         sheet = wb.worksheets[sheet_name]
#     else:
#         sheet = wb[sheet_name]
#     data = list(sheet.values)
#     df = pd.DataFrame(data)
#     return df

# #############################
# # 3. Функция для проверки грейдов
# #############################
# def check_grades(df, allowed_grades):
#     unknown_grades = set()
#     for col in df.columns:
#         if len(df) > 2:
#             third_row_value = df.iloc[2, col]
#             if pd.notna(third_row_value):
#                 text = str(third_row_value).strip().lower()
#                 if text in ["inside", "outside"]:
#                     grade_val = df.iloc[1, col]
#                     if pd.notna(grade_val):
#                         grade_str = str(grade_val).strip()
#                         if grade_str not in allowed_grades:
#                             unknown_grades.add(grade_str)
#     return unknown_grades

# #############################
# # 4. Остальные функции
# #############################
# def find_total_cost_column_name(df):
#     for col in df.columns:
#         cell_value = df.iloc[1, col]
#         if pd.notna(cell_value) and str(cell_value).strip() == "Total cost":
#             return col
#     return None

# def process_function_name(epic_name):
#     # Заменяем пробелы на нижние подчёркивания
#     return "_".join(epic_name.split())

# #############################
# # 5. Обработка "с эпиками"
# #############################
# def process_with_epics(df):
#     total_cost_col = find_total_cost_column_name(df)
#     start_row = 7  # Подберите под вашу структуру

#     # Берём только столбцы B и C
#     df_subset = df.iloc[start_row:, [1, 2]].dropna(how='all').reset_index(drop=True)
#     df_subset.columns = ['Feature', 'Details']

#     summary_list = []
#     custom_link_id_list = []
#     parent_link_id_list = []
#     issue_type_list = []
#     total_cost_list = []
#     function_name_list = []  # новый столбец для Function name

#     current_custom_link_id = None
#     current_function_name = None

#     for idx, row in df_subset.iterrows():
#         feature = row['Feature']
#         detail = row['Details']
#         original_row_index = idx + start_row

#         cost_value = None
#         if total_cost_col is not None and original_row_index < len(df):
#             cost_value = df.iloc[original_row_index, total_cost_col]

#         # Если строка с Эпиком (Feature заполнен)
#         if pd.notna(feature):
#             custom_id = str(random.randint(100000, 999999))
#             processed_fn = process_function_name(str(feature))
#             summary_list.append(feature)  # для эпика оставляем исходное название
#             issue_type_list.append("Epic")
#             custom_link_id_list.append(custom_id)
#             parent_link_id_list.append(None)
#             total_cost_list.append(None)
#             function_name_list.append(processed_fn)
#             current_custom_link_id = custom_id
#             current_function_name = processed_fn

#         # Если строка с ФТ (Details заполнен)
#         if pd.notna(detail):
#             summary_list.append(detail)  # теперь только значение из столбца C
#             issue_type_list.append("ФТ")
#             custom_link_id_list.append(None)
#             parent_link_id_list.append(current_custom_link_id)
#             total_cost_list.append(cost_value if pd.notna(cost_value) else None)
#             # Для ФТ берём последнее известное значение Function name
#             function_name_list.append(current_function_name if current_function_name is not None else None)

#     result_df = pd.DataFrame({
#         'Summary': summary_list,
#         'Custom Link ID': custom_link_id_list,
#         'Parent Link ID': parent_link_id_list,
#         'Issue Type': issue_type_list,
#         'Total cost': total_cost_list,
#         'Function name': function_name_list
#     })

#     return result_df

# #############################
# # 6. Обработка "без эпиков"
# #############################
# def process_without_epics(df):
#     total_cost_col = find_total_cost_column_name(df)
#     start_row = 7

#     df_subset = df.iloc[start_row:, [1, 2]].dropna(how='all').reset_index(drop=True)
#     df_subset.columns = ['Feature', 'Details']

#     summary_list = []
#     total_cost_list = []
#     function_name_list = []
#     current_function_name = None

#     for idx, row in df_subset.iterrows():
#         original_row_index = idx + start_row
#         cost_value = None
#         if total_cost_col is not None and original_row_index < len(df):
#             cost_value = df.iloc[original_row_index, total_cost_col]

#         if pd.notna(row['Feature']):
#             current_function_name = process_function_name(str(row['Feature']))

#         if pd.notna(row['Details']):
#             summary_list.append(row['Details'])
#             total_cost_list.append(cost_value if pd.notna(cost_value) else None)
#             function_name_list.append(current_function_name if current_function_name is not None else None)

#     result_df = pd.DataFrame({
#         'Summary': summary_list,
#         'Issue Type': ['ФТ'] * len(summary_list),
#         'Total cost': total_cost_list,
#         'Function name': function_name_list
#     })

#     return result_df

# #############################
# # 7. Основной поток (Streamlit)
# #############################
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

#         # Проверяем грейды (для предупреждения, если найдены неизвестные)
#         unknown_grades = check_grades(df, allowed_grades)
#         if unknown_grades:
#             st.warning(
#                 "Внимание! В смете присутствуют неизвестные грейды: " + ", ".join(unknown_grades)
#             )

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









# ВЕРСИЯ 0.2

# import streamlit as st
# import pandas as pd
# import random
# from io import BytesIO
# import openpyxl

# #############################
# # 1. Список допустимых грейдов
# #############################
# allowed_grades = [
#     "Продуктовая аналитика стажер",
#     "UX-аналитик junior",
#     "UX-аналитик middle -",
#     "UX-аналитик middle",
#     "UX-аналитик senior",
#     "Web/mobile-аналитик junior",
#     "Web/mobile-аналитик middle -",
#     "Web/mobile-аналитик middle",
#     "Web/mobile-аналитик middle +",
#     "Web/mobile-аналитик senior",
#     "Web/mobile-аналитик TL",
#     "BI/data-аналитик junior",
#     "BI/data-аналитик middle",
#     "BI/data-аналитик middle +",
#     "BI/data-аналитик senior",
#     "Product manager junior",
#     "Product manager middle",
#     "Product manager middle +",
#     "Product manager Senior",
#     "Web/mobile-analyst middle",
#     "Web/mobile-analyst senior",
#     "Дизайнер стажер",
#     "Дизайнер junior-",
#     "Дизайнер junior",
#     "Дизайнер junior+",
#     "Дизайнер middle-",
#     "Дизайнер middle",
#     "Дизайнер middle+",
#     "Дизайнер senior",
#     "Дизайнер senior+",
#     "Art Director",
#     "Web middle",
#     "Web senior",
#     "Системный аналитик Стажер",
#     "Системный аналитик junior-",
#     "Системный аналитик junior",
#     "Системный аналитик junior+",
#     "Системный аналитик middle-",
#     "Системный аналитик middle",
#     "Системный аналитик middle+",
#     "Системный аналитик senior",
#     "Системный аналитик senior+",
#     "Системный аналитик lead",
#     "Проектировщик стажер",
#     "Проектировщик junior",
#     "Проектировщик middle",
#     "Проектировщик middle+",
#     "Проектировщик senior",
#     "Проектировщик senior+",
#     "Проектировщик lead",
#     "System analyst middle",
#     "System analyst senior",
#     "SEO",
#     "tech.writer",
#     "UX writer",
#     "PM стажер",
#     "PM intern",
#     "PM junior",
#     "PM junior+",
#     "PM middle",
#     "PM middle+",
#     "PM senior",
#     "PM senior+",
#     "GH",
#     "PMO",
#     "Bitrix junior",
#     "Bitrix junior+",
#     "Bitrix middle-",
#     "Bitrix middle",
#     "Bitrix middle+",
#     "Bitrix senior-",
#     "Bitrix senior",
#     "Bitrix senior+",
#     "Bitrix teamlead -",
#     "Bitrix teamlead",
#     "Bitrix teamlead +",
#     "Bitrix teamlead grouphead -",
#     "Bitrix teamlead grouphead",
#     "Bitrix teamlead grouphead +",
#     "Bitrix middle",
#     "Bitrix senior",
#     "Разработка стажер",
#     "Framework junior",
#     "Framework junior+",
#     "Framework middle-",
#     "Framework middle",
#     "Framework middle+",
#     "Framework senior-",
#     "Framework senior",
#     "Framework senior+",
#     "Framework teamlead -",
#     "Framework teamlead",
#     "Framework teamlead +",
#     "Framework teamlead grouphead -",
#     "Framework teamlead grouphead",
#     "Framework teamlead grouphead +",
#     "Framework middle",
#     "Framework senior",
#     "QA junior-",
#     "QA junior",
#     "QA junior +",
#     "QA middle-",
#     "QA middle",
#     "QA middle+",
#     "QA senior -",
#     "QA senior",
#     "QA Teamlead",
#     "AQA junior-",
#     "AQA junior",
#     "AQA junior +",
#     "AQA middle-",
#     "AQA middle",
#     "AQA middle+",
#     "AQA senior -",
#     "AQA senior",
#     "AQA teamlead",
#     "QA middle",
#     "QA senior",
#     "QA AT Middle",
#     "QA AT Senior",
#     "Front-end junior",
#     "Front-end junior +",
#     "Front-end middle -",
#     "Front-end middle",
#     "Front-end middle +",
#     "Front-end senior -",
#     "Front-end senior",
#     "Front-end senior +",
#     "Front-end teamlead",
#     "NodeJS junior",
#     "NodeJS junior +",
#     "NodeJS middle -",
#     "NodeJS middle",
#     "NodeJS middle +",
#     "NodeJS senior -",
#     "NodeJS senior",
#     "NodeJS senior +",
#     "NodeJS teamlead",
#     "Front-end html/css middle -",
#     "Front-end html/css middle",
#     "Front-end html/css middle +",
#     "Front-end middle",
#     "Front-end senior",
#     "NodeJS middle",
#     "NodeJS senior",
#     "Front-end html/css middle",
#     "Mobile Dev Junior-",
#     "Mobile Dev Junior",
#     "Mobile Dev Junior+",
#     "Mobile Dev Middle-",
#     "Mobile Dev Middle",
#     "Mobile Dev Middle+",
#     "Mobile Dev Senior-",
#     "Mobile Dev Senior",
#     "Mobile Dev Senior+",
#     "Mobile Dev Teamlead",
#     "Mobile dev middle",
#     "Mobile dev senior",
#     "Python junior",
#     "Python middle-",
#     "Python middle",
#     "Python middle+",
#     "Python senior-",
#     "Python senior",
#     "Python senior+",
#     "Python teamlead",
#     "Golang junior",
#     "Golang middle-",
#     "Golang middle",
#     "Golang middle+",
#     "Golang senior-",
#     "Golang senior",
#     "Golang senior+",
#     "Golang teamlead",
#     "Python middle",
#     "Python senior",
#     "Golang middle",
#     "Golang senior",
#     "Devops junior",
#     "Devops middle-",
#     "Devops middle",
#     "Devops middle+",
#     "Devops senior-",
#     "Devops senior",
#     "Devops senior+",
#     "Devops teamlead",
#     "Devops middle",
#     "Devops senior",
#     "Java middle",
#     "Java senior",
#     ".NET",
#     ".NET Senior",
#     "Security Specialist",
#     "Lead Programmer Researcher / AI",
#     "Programmer researcher / AI",
#     "Senior data analyst / AI",
#     "Middle data analyst / AI",
#     "Junior data analyst / AI",
#     "PM / AI",
#     "Teamlead / AI",
#     "Product analyst / AI",
#     "Solution Architect consultant / AI",
#     "Pr-manager junior",
#     "Pr-manager middle",
#     "Pr-manager senior",
#     "DevRel junior",
#     "DevRel middle",
#     "DevRel senior",
#     "Copywriter middle",
#     "Copywriter senior",
#     "Photographer/Videographer",
#     "Copywriter middle",
#     "Copywriter senior",
#     "Content Manager",
# ]

# #############################
# # 2. Чтение Excel (с формулами как значениями)
# #############################
# def read_excel_data_only(file, sheet_name=0):
#     file_data = file.read()
#     wb = openpyxl.load_workbook(BytesIO(file_data), data_only=True)
#     if isinstance(sheet_name, int):
#         sheet = wb.worksheets[sheet_name]
#     else:
#         sheet = wb[sheet_name]

#     data = list(sheet.values)
#     df = pd.DataFrame(data)
#     return df

# #############################
# # 3. Функция для проверки грейдов
# #############################
# def check_grades(df, allowed_grades):
#     """
#     Проверяем в 3-й строке (индекс 2) ячейки на значения "Inside" или "Outside".
#     Если находим такие ячейки, значит во 2-й строке (индекс 1) лежит грейд.
#     Сравниваем грейд со списком allowed_grades.
#     Если находим незнакомый грейд, собираем в множество unknown_grades.
#     Возвращаем множество unknown_grades (или пустое множество).
#     """
#     unknown_grades = set()

#     # Перебираем все столбцы df
#     for col in df.columns:
#         # Смотрим, что написано в 3-й строке (индекс 2)
#         if len(df) > 2:  # чтобы не выйти за границы, если таблица меньше 3 строк
#             third_row_value = df.iloc[2, col]
#             if pd.notna(third_row_value):
#                 text = str(third_row_value).strip().lower()
#                 # Если "Inside" или "Outside", значит в строке выше (index=1) лежит грейд
#                 if text in ["inside", "outside"]:
#                     # Читаем грейд
#                     grade_val = df.iloc[1, col]
#                     if pd.notna(grade_val):
#                         grade_str = str(grade_val).strip()
#                         # Сравниваем с списком
#                         if grade_str not in allowed_grades:
#                             unknown_grades.add(grade_str)

#     return unknown_grades

# #############################
# # 4. Остальные функции
# #############################
# def find_total_cost_column_name(df):
#     for col in df.columns:
#         cell_value = df.iloc[1, col]
#         if pd.notna(cell_value) and str(cell_value).strip() == "Total cost":
#             return col
#     return None

# def process_with_epics(df):
#     total_cost_col = find_total_cost_column_name(df)
#     start_row = 7  # TODO

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
#         original_row_index = idx + start_row

#         cost_value = None
#         if total_cost_col is not None and original_row_index < len(df):
#             cost_value = df.iloc[original_row_index, total_cost_col]

#         if pd.notna(feature):
#             summary_list.append(feature)
#             issue_type_list.append("Epic")
#             custom_id = str(random.randint(100000, 999999))
#             custom_link_id_list.append(custom_id)
#             parent_link_id_list.append(None)
#             total_cost_list.append(None)
#             current_custom_link_id = custom_id
#             current_epic_name = feature

#         if pd.notna(detail):
#             if current_epic_name:
#                 ft_summary = f"[{current_epic_name}] {detail}"
#             else:
#                 ft_summary = detail

#             summary_list.append(ft_summary)
#             issue_type_list.append("ФТ")
#             custom_link_id_list.append(None)
#             parent_link_id_list.append(current_custom_link_id)
#             total_cost_list.append(cost_value if pd.notna(cost_value) else None)

#     return pd.DataFrame({
#         'Summary': summary_list,
#         'Custom Link ID': custom_link_id_list,
#         'Parent Link ID': parent_link_id_list,
#         'Issue Type': issue_type_list,
#         'Total cost': total_cost_list
#     })

# def process_without_epics(df):
#     total_cost_col = find_total_cost_column_name(df)
#     start_row = 7

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

#         if pd.notna(feature):
#             current_epic_name = feature

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

# #############################
# # 5. Основной поток (Streamlit)
# #############################
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

#         # Сначала проверяем грейды
#         unknown_grades = check_grades(df, allowed_grades)
#         if unknown_grades:
#             st.warning(
#                 "Внимание! В смете присутствуют неизвестные грейды: "
#                 + ", ".join(unknown_grades)
#             )

#         # Затем продолжаем обычную обработку
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
