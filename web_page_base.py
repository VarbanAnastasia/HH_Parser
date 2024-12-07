from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from hh_config import HHConfig
from typing import List
from selenium.webdriver.remote.webelement import WebElement
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BasePage:
    """Базовый класс для работы с веб-страницами"""

    class Locators:
        JOB_TITLES = '//span[@data-qa="serp-item__title-text"]'
        JOB_LINKS = '//a[@data-qa="serp-item__title"]'
        PAGES = '//ul[contains(@class,"magritte-number-pages-container")]/li'
        COMPANIES = '//span[@data-qa="vacancy-serp__vacancy-employer-text"]'
        CITIES = '//span[@data-qa="vacancy-serp__vacancy-address"]'
        BUTTON_CLOSE_NOTIFICATIONS = '//div[@class="bloko-notification__close"]'

    def __init__(self, timeout: int = 5):
        """Инициализация базового класса

        Args:
            timeout (int): Время ожидания элементов (по умолчанию 10 секунд)
        """
        self.config = HHConfig()
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service)

        self.browser.implicitly_wait(timeout)
        self.wait = WebDriverWait(self.browser, timeout)
        self.logger = logging.getLogger(__name__)

    def find_element(self, locator: str) -> WebElement:
        """Поиск элемента с явным ожиданием

        Args:
            locator (str): XPath локатор элемента
        """
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
        except TimeoutException:
            self.logger.error(f"Элемент не найден: {locator}")
            raise

    def find_elements(self, locator: str) -> List[WebElement]:
        """Поиск элементов с явным ожиданием

        Args:
            locator (str): XPath локатор элементов
        """
        try:
            return self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, locator))
            )
        except TimeoutException:
            self.logger.error(f"Элементы не найдены: {locator}")
            raise

    def close_notification(self):
        """Закрытие уведомления, если оно присутствует"""
        try:
            element = self.find_element(self.Locators.BUTTON_CLOSE_NOTIFICATIONS)
            ActionChains(self.browser).move_to_element(element).click().perform()
            self.logger.info("Уведомление закрыто")
        except TimeoutException:
            self.logger.info("Уведомление не найдено")
            pass

    def get_element_text(self, element, retries: int = 5) -> str:
        """
        Получение текста элемента с повторными попытками
        Args:
            element: WebElement
            retries (int): Количество попыток
        """
        for attempt in range(retries):
            try:
                return element.text
            except StaleElementReferenceException as e:
                if attempt == retries - 1:
                    self.logger.error(f"Не удалось получить текст после {retries} попыток")
                    raise
                self.logger.warning(f"Попытка {attempt + 1} не удалась: {e}")
        return ""

    def is_element_present(self, locator: str) -> bool:
        """Проверка наличия элемента на странице

        Args:
            locator (str): XPath локатор элемента
        """
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False

    def get_page_url(self, page: int) -> str:
        """Получение URL для конкретной страницы

        Args:
            page (int): Номер страницы

        """
        return self.config.get_url_for_page(page)

    def extract_max_page(self) -> int:
        """Получение максимального количества страниц с результатами поиска"""
        pages = len(self.find_elements(BasePage.Locators.PAGES))
        return pages

    def go_to_page(self, page: int):
        """Переход на указанную страницу с обработкой ошибок"""
        try:
            xpath = f'//a[contains(@data-qa,"pager-page") and text()="{page}"]'
            page_link = self.find_element(xpath)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.browser.execute_script("arguments[0].scrollIntoView(true);", page_link)
            self.browser.execute_script("arguments[0].click();", page_link)
            time.sleep(5)
        except Exception as e:
            self.logger.error(f"Ошибка при переходе на страницу {page}: {e}")
            raise
        