import os
import sys
import json
import time
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import codecs
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .Parser import Parser
sys.path.insert(1, os.path.join(sys.path[0], '../'))
from database.dbworker import init_post

today = date.today()

from pyvirtualdisplay import Display #//for cli VPS

config = configparser.ConfigParser()
config.read("config.ini")

# filename='parser.log'
logging.basicConfig(encoding='utf-8', format=config['Logging']['Format'], level=logging.INFO)

class RBCParser(Parser):
    src_news_list = list()
    source_site = 'RBC'
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    def rbc_all_news_href_business(self, n) -> 'list of news href from RBC':
        try:
            logMessage = self.virtual_display()
            logging.info(logMessage)
            driver = webdriver.Chrome(desired_capabilities=self.caps, service=self.service, options=self.options)

            driver.get(self.url)
            time.sleep(1)

            def click_top_up_btn(n:int):
                for i in range(n):
                    last_height = driver.execute_script("return document.body.scrollHeight")
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

            click_top_up_btn(n=n)

            posts = driver.find_elements(by=By.XPATH, value='//a[@class="item__link"]')

            for data in posts:
                self.src_news_list.append(data.get_attribute('href'))
            time.sleep(0.1)

        except Exception as e:
            logging.error(e)

        finally:
            driver.close()
            driver.quit()


    def rbc_get_posts(self):
        try:
            logMessage = self.virtual_display()
            logging.info(logMessage)
            driver = webdriver.Chrome(service=self.service, options=self.options)

            for href in self.src_news_list:
                driver.get(href)
                time.sleep(0.5)
                title = driver.find_element(by=By.XPATH, value='//h1[@itemprop="headline"]')
                articleBody = driver.find_element(by=By.XPATH, value='//div[@itemprop="articleBody"]')
                data = articleBody.find_elements(by=By.TAG_NAME, value='p')
                text = ''
                for p in data:
                    text += p.text

                codecs.encode(text, encoding='utf-8')
                data_time = driver.find_element(by=By.XPATH, value='//time[@itemprop="datePublished"]')
                views = driver.find_element(by=By.XPATH, value='//div[@class="article__header__counter-block"]')
                watches = views.text.replace(' ', '')

                log_message = init_post(title=str(title.text),href=str(href),text=str(text),date_time=str(data_time.text),source_site=self.source_site,views=int(watches), is_send=False)
                logging.info(log_message)

        except Exception as e:
            return e

        finally:
            driver.close()
            driver.quit()




