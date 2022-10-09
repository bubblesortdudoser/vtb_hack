import logging
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pyvirtualdisplay import Display #//for cli VPS

config = configparser.ConfigParser()
config.read("config.ini")

# filename='parser.log'
logging.basicConfig(encoding='utf-8', format=config['Logging']['Format'], level=logging.INFO)

class Parser:
    interfax_business_url = 'https://www.interfax.ru/business/'
    # rbc_economics = ['https://www.rbc.ru/economics/', 'https://www.rbc.ru/business/?utm_source=topline', 'https://www.rbc.ru/finances/?utm_source=topline', 'https://www.rbc.ru/politics/?utm_source=topline']
    rbc_economics = 'https://www.rbc.ru/politics/?utm_source=topline'
    DRIVER = config['Selenium']['driver']
    service = Service('/home/donqhomo/Desktop/vtb_hack/app/chromedriver')
    options = webdriver.ChromeOptions()

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



        





