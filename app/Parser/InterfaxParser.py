import os
import sys
import json
import time
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from .Parser import Parser
sys.path.insert(1, os.path.join(sys.path[0], '../'))
from database.dbworker import init_post

from pyvirtualdisplay import Display #//for cli VPS

config = configparser.ConfigParser()
config.read("config.ini")

# filename='parser.log'
logging.basicConfig(encoding='utf-8', format=config['Logging']['Format'], level=logging.INFO)

class InterfaxParser(Parser):
    def interfax_all_news_href_business(self) -> 'list of news href from interfax':
        try:
            logMessage = self.virtual_display()
            logging.info(logMessage)
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(self.interfax_business_url)
            time.sleep(1)

            timeline__text = driver.find_elements(by=By.XPATH, value='//div[@class="timeline__text"]')
            timeline__group = driver.find_elements(by=By.XPATH, value='//div[@class="timeline__group"]')
            timeline__photo = driver.find_elements(by=By.XPATH, value='//div[@class="timeline__photo"]')

            def click_top_up_btn(n:int):
                for i in range(n):
                    btn = driver.find_element(by=By.XPATH, value='//div[@class="timeline__more"]')
                    src = btn.get_attribute('onclick')
                    driver.execute_script(src)
                    logging.info(f"click: {i}")
                    time.sleep(0.1)

            click_top_up_btn(n=500)

            for post in timeline__text:
                src = post.find_elements(by=By.TAG_NAME, value="a")
                for href in src:
                    self.src_news_list.append(href.get_attribute('href'))

            for post in timeline__group:
                src = post.find_elements(by=By.TAG_NAME, value="a")
                for href in src:
                    self.src_news_list.append(href.get_attribute('href'))

            for post in timeline__photo:
                src = post.find_elements(by=By.TAG_NAME, value="a")
                for href in src:
                    self.src_news_list.append(href.get_attribute('href'))

            logging.info(f"href list: {self.src_news_list}")
            dublicate = dict((x, self.src_news_list.count(x)) for x in set(self.src_news_list) if self.src_news_list.count(x) > 1)
            logging.info(f'Len: {len(self.src_news_list)}| Duplicate: {dublicate}')
            self.src_news_list = list(set(self.src_news_list))
            return self.src_news_list

        except Exception as e:
            logging.error(e)

        finally:
            driver.close()
            driver.quit()

    def interfax_get_posts(self):
        try:
            logMessage = self.virtual_display()
            logging.info(logMessage)
            driver = webdriver.Chrome(service=self.service, options=self.options)

            text = ''
            for href in self.src_news_list:
                driver.get(href)
                time.sleep(0.5)
                title = driver.find_element(by=By.XPATH, value='//h1[@itemprop="headline"]')
                p = driver.find_elements(by=By.TAG_NAME, value='p')
                for data in p:
                    text += data.text
                time_block = driver.find_element(by=By.XPATH, value='//aside[@class="textML"]')
                data_time = time_block.find_element(by=By.TAG_NAME, value='time').get_attribute('datetime')
                log_message = init_post(title=str(title.text),href=str(href),text=str(text),date_time=str(data_time))

                logging.info(log_message)

        except Exception as e:
            return e

        finally:
            driver.close()
            driver.quit()

