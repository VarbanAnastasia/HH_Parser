from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import logging
from selenium.common.exceptions import StaleElementReferenceException

# Настраиваем логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage:
    BASE_URL = 'https://hh.ru/search/vacancy?text=Qa+automation+engineer&page=0&excluded_text=java&items_on_page=100'

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='D:\Python\chromedriver.exe')
        self.browser.implicitly_wait(3)

    def __del__(self):
        self.browser.quit()

    JOB_TITLES = '//span[@data-qa="serp-item__title-text"]'
    JOB_LINKS = '//a[@data-qa="serp-item__title"]'
    PAGES = '//ul[contains(@class,"magritte-number-pages-container")]/li'
    COMPANIES = '//span[@data-qa="vacancy-serp__vacancy-employer-text"]'
    CITIES = '//span[@data-qa="vacancy-serp__vacancy-address"]'
    SPECIFIC_PAGE = '//a[contains(@data-qa,"number-pages-{number_page}")]'
    BUTTON_CLOSE_NOTIFICATIONS = '//div[@class="bloko-notification__close"]'

    def close_notification(self):
        element = self.browser.find_element(By.XPATH, self.BUTTON_CLOSE_NOTIFICATIONS)
        ActionChains(self.browser).move_to_element(element).click().perform()

    def get_element_text(self, element, retries=5):
        """Получает текст элемента, повторяя попытку при StaleElementReferenceException."""
        attempt = 0
        while attempt < retries:
            try:
                text = element.text
                # logger.info(f"Успешно получен текст: {text}")
                return text
            except StaleElementReferenceException as e:
                attempt += 1
                logger.warning(f"Попытка {attempt} получить текст элемента не удалась: {e}")
                if attempt == retries:
                    logger.error("Не удалось получить текст элемента после максимального количества попыток")
                    raise  # Выбросить исключение после исчерпания попыток

        return ""
