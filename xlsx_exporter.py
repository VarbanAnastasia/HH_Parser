from vacancy_parser import job_titles, company_names, company_locations, job_links
from openpyxl import Workbook


def save_to_excel(titles, names, locations, links, filename='hh_data.xlsx'):
    # Создаем новую рабочую книгу Excel
    wb = Workbook()
    # Получаем активный лист
    ws = wb.active
    # Задаем название листа
    ws.title = "Вакансии"

    # Создаем список заголовков для столбцов
    headers = ['#', 'Job Title', 'Company Name', 'Company Location', 'Link']
    # Добавляем заголовки в первую строку
    ws.append(headers)

    # Проходим по всем данным, используя минимальную длину списков чтобы избежать ошибок
    for i in range(min(len(titles), len(names), len(locations), len(links))):
        # Добавляем строку с данными: номер, название вакансии, компания, локация и ссылка
        ws.append([i + 1, titles[i], names[i], locations[i], links[i]])

    # Сохраняем файл с указанным именем
    wb.save(filename)


# Вызываем функцию save_to_excel для сохранения данных в Excel файл
save_to_excel(
    titles=job_titles,
    names=company_names,
    locations=company_locations,
    links=job_links
)
# Выводим сообщение об успешном создании файла
print("Файл успешно создан")
