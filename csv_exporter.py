import csv
from vacancy_parser import job_titles, company_names, company_locations, job_links


def write_to_csv(titles, names, locations, links):
    with open('hh_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['#', 'Job Title', 'Company Name', 'Company Location', 'Link'])
        for i in range(min(len(titles), len(names), len(locations), len(links))):
            writer.writerow([i+1, titles[i], names[i], locations[i], links[i]])

write_to_csv(titles=job_titles, names=company_names, locations=company_locations, links=job_links)
