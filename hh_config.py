from typing import Dict
from urllib.parse import urlencode

class HHConfig:
    """
    Конфигурация для работы с API hh.ru"""
    def __init__(self):
        self.BASE_URL: str = 'https://hh.ru'
        self.SEARCH_PATH: str = '/search/vacancy'
        self.SEARCH_PARAMS: Dict[str, any] = {
            'text': 'Qa automation engineer',
            'excluded_text': 'java',
            'items_on_page': 100,
            'page': 0
        }
    
    @property
    def full_url(self, text: str = None, excluded_text: str = None) -> str:
        """Формирует полный URL с параметрами
        Args:
            text (str, optional): Поисковый запрос. По умолчанию используется значение из SEARCH_PARAMS
            excluded_text (str, optional): Исключаемый текст. По умолчанию используется значение из SEARCH_PARAMS
        """
        params = self.SEARCH_PARAMS.copy()
        if text is not None:
            params['text'] = text
        if excluded_text is not None:
            params['excluded_text'] = excluded_text
            
        return f"{self.BASE_URL}{self.SEARCH_PATH}?{urlencode(self.SEARCH_PARAMS)}"
    
    def get_url_for_page(self, page: int) -> str:
        """
        Формирует URL для конкретной страницы
        
        Args:
            page (int): Номер страницы
        """
        params = self.SEARCH_PARAMS.copy()
        params['page'] = page
        return f"{self.BASE_URL}{self.SEARCH_PATH}?{urlencode(params)}"