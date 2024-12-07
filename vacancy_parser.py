from web_page_base import BasePage
import logging


class Parser(BasePage):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.browser.get(self.get_page_url(page=1))
        self.close_notification()

    def extract_hh_jobs(self):
        """Получаем названия вакансий"""
        titles = []

        for page in range(1, self.extract_max_page() + 1):
            self.go_to_page(page=page)
            jobs = self.find_elements(BasePage.Locators.JOB_TITLES)
            titles.extend([self.get_element_text(job) for job in jobs])

        return titles

    def extract_hh_links(self):
        """Получаем ссылки вакансий"""
        try:
            self.go_to_page(page=1)
            self.browser.set_page_load_timeout(10)
            links = []

            for page in range(1, self.extract_max_page() + 1):
                self.logger.info(f"Обработка страницы {page}")
                self.go_to_page(page=page)
                jobs = self.find_elements(BasePage.Locators.JOB_LINKS)
                links.extend([job.get_attribute('href') for job in jobs])

            self.logger.info(f"Всего найдено ссылок: {len(links)}")
            return links
        except Exception as e:
            self.logger.error(f"Ошибка при получении ссылок: {e}")
            raise

    def extract_company_name(self):
        """Получаем названия компаний"""
        names = []

        for page in range(1, self.extract_max_page() + 1):
            self.go_to_page(page=page)
            elements = self.find_elements(BasePage.Locators.COMPANIES)
            companies = [self.get_element_text(element) for element in elements]
            names.extend([companies[i] for i in range(len(companies)) if i % 2 == 0])

        return names

    def extract_company_location(self):
        """Получаем местоположение компаний"""
        locations = []

        for page in range(1, self.extract_max_page() + 1):
            self.go_to_page(page=page)
            loc = [self.get_element_text(loc) for loc in self.find_elements(BasePage.Locators.CITIES)]
            result = [loc[i] for i in range(len(loc)) if i % 2 != 0]
            locations.extend([result[i] for i in range(len(result)) if i % 2 == 0])

        return locations


parser = Parser()
job_titles = parser.extract_hh_jobs()
company_names = parser.extract_company_name()
company_locations = parser.extract_company_location()
job_links = parser.extract_hh_links()
