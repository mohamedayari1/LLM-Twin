import time
from abc import ABC, abstractmethod
from tempfile import mkdtemp  



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
from db.documents import BaseDocument

class BaseCrawler(ABC):
    model: type[BaseDocument]
    
    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...