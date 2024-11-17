import pandas as pd
import random


def extract_and_prepare_jira_csv(file_path):
    # Шаг 1: Загружаем исходный Excel файл и извлекаем нужные столбцы B и C с 7 строки
    df = pd.read_excel(file_path, sheet_name='Смета 0.1')

    # Извлекаем содержимое столбцов B и C, начиная с 7 строки
    df_subset = df.iloc[6:, [1, 2]].dropna(how='all').reset_index(drop=True)
    df_subset.columns = ['Feature', 'Details']

    # Шаг 2: Формируем итоговый CSV для импорта в Jira
    summary_list = []
    custom_link_id_list = []
    parent_link_id_list = []
    issue_type_list = []

    current_custom_link_id = None

    # Перебираем строки и заполняем итоговые списки
    for index, row in df_subset.iterrows():
        feature = row['Feature']
        detail = row['Details']

        # Если есть значение в столбце Feature, создаём новую запись с типом "Story"
        if pd.notna(feature):
            summary_list.append(feature)
            issue_type_list.append("Story")
            custom_id = str(random.randint(100000, 999999))
            custom_link_id_list.append(custom_id)
            parent_link_id_list.append(None)  # Для "Story" Parent Link ID не заполняется
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

    # Сохраняем в CSV файл
    output_path = 'Final_Jira_Import.csv'
    final_df.to_csv(output_path, index=False)

    print(f"Файл '{output_path}' успешно создан.")
    return final_df


# Пример использования
file_path = 'Шаблон оценки v2 (actual).xlsx'  # Укажи путь к твоему файлу
extract_and_prepare_jira_csv(file_path)
