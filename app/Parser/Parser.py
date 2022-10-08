import os
import sys
import time
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display #//for cli VPS

config = configparser.ConfigParser()
config.read("config.ini")

# filename='parser.log'
logging.basicConfig(encoding='utf-8', format=config['Logging']['Format'], level=logging.INFO)

class Parser:
    interfax_business_url = 'https://www.interfax.ru/business/'
    DRIVER = config['Selenium']['driver']
    service = Service('/home/donqhomo/Desktop/vtb_hack/app/chromedriver')
    options = webdriver.ChromeOptions()

    news = list()

    def __init__(self, debug:bool):
        self.debug = debug

    def virtual_display(self):
        try:
            if self.debug == False:
                self.options.add_argument("--no-sandbox");
                self.options.add_argument("--disable-dev-shm-usage");
                display = Display(visible=0, size=(800, 800))
                display.start()
                return {f'message': 'Debug={self.debug}; virtual display -> ON | Start args: --no-sandbox --disable-dev-shm-usage'}
            else:
                logging.level = logging.DEBUG
                return {'message': 'virtual display -> OFF | --sandbox'}
        
        except Exception as e:
            logging.error(e)

    def interfax_all_news_business(self) -> 'News from interfax':
        try:
            logMessage = self.virtual_display()
            logging.info(logMessage)
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(self.interfax_business_url)
            time.sleep(1)
            driver.find_element(by=By, value="sf_url")

        except Exception as e:
            logging.error(e)

        finally:
            driver.close()
            driver.quit()

        





