from web_page_base import *
import time
from web_page_base import BasePage
import logging


class Parser(BasePage):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def extract_max_page(self):
        pages = len(self.browser.find_elements(By.XPATH, self.PAGES))
        return pages

    def go_to_page(self, page: int):
        """Переход на указанную страницу с обработкой ошибок"""
        try:
            xpath = f'//a[contains(@data-qa,"pager-page") and text()="{page}"]'
            page_link = self.browser.find_element(By.XPATH, xpath)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", page_link)
            self.browser.execute_script("arguments[0].click();", page_link)
            time.sleep(5)
        except Exception as e:
            self.logger.error(f"Ошибка при переходе на страницу {page}: {e}")
            raise

    def extract_hh_jobs(self):
        """Получаем названия вакансий"""
        self.browser.get(self.BASE_URL)
        self.close_notification()
        titles = []

        for page in range(1, self.extract_max_page() + 1):
            self.go_to_page(page=page)
            jobs = self.browser.find_elements(By.XPATH, self.JOB_TITLES)
            titles.extend([self.get_element_text(job) for job in jobs])

        return titles

    def extract_hh_links(self):
        """Получаем ссылки вакансий"""
        try:
            self.browser.get(self.BASE_URL)
            self.browser.set_page_load_timeout(10)
            links = []

            for page in range(1, self.extract_max_page() + 1):
                self.logger.info(f"Обработка страницы {page}")
                self.go_to_page(page=page)
                jobs = self.browser.find_elements(By.XPATH, self.JOB_LINKS)
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
            elements = self.browser.find_elements(By.XPATH, self.COMPANIES)
            companies = [self.get_element_text(element) for element in elements]
            names.extend([companies[i] for i in range(len(companies)) if i % 2 == 0])

        return names

    def extract_company_location(self):
        """Получаем местоположение компаний"""
        locations = []

        for page in range(1, self.extract_max_page() + 1):
            self.go_to_page(page=page)
            loc = [self.get_element_text(loc) for loc in self.browser.find_elements(By.XPATH, self.CITIES)]
            result = [loc[i] for i in range(len(loc)) if i % 2 != 0]
            locations.extend([result[i] for i in range(len(result)) if i % 2 == 0])

        return locations


parser = Parser()
job_titles = parser.extract_hh_jobs()
company_names = parser.extract_company_name()
company_locations = parser.extract_company_location()
job_links = parser.extract_hh_links()
