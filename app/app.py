import configparser
from Parser import *

import requests
from database.dbworker import get_all_posts, change_status, to_csv, unsend_posts

config = configparser.ConfigParser()
config.read("config.ini")

class App():

    def first_start(self):
        rbc_urls = ['https://www.rbc.ru/economics/', 'https://www.rbc.ru/business/?utm_source=topline',
                         'https://www.rbc.ru/finances/?utm_source=topline',
                         'https://www.rbc.ru/politics/?utm_source=topline']
        for i in range(len(rbc_urls)):
            rbc = RBCParser(url = rbc_urls[i], debug=True)
            rbc.rbc_all_news_href_business(n=100)
            rbc.rbc_get_posts()

        interfax = InterfaxParser(debug=True, url ='https://www.interfax.ru/business/')
        interfax.interfax_all_news_href_business(n=30)
        interfax.interfax_get_posts()

        to_csv()
        posts = get_all_posts()
        for post in posts:
            change_status(href = post.href, status=True)

    def polling(self):
        try:
            while True:
                rbc_urls = ['https://www.rbc.ru/economics/', 'https://www.rbc.ru/business/?utm_source=topline',
                            'https://www.rbc.ru/finances/?utm_source=topline',
                            'https://www.rbc.ru/politics/?utm_source=topline']
                for i in range(len(rbc_urls)):
                    rbc = RBCParser(url=rbc_urls[i], debug=True)
                    rbc.rbc_all_news_href_business(n=2)
                    rbc.rbc_get_posts()

                interfax = InterfaxParser(debug=True, url='https://www.interfax.ru/business/')
                interfax.interfax_all_news_href_business(n=2)
                interfax.interfax_get_posts()
        except Exception as e:
            pass


app = App()
# app.first_start()
app.polling()



