import configparser
from Parser import *
from database.dbworker import to_csv
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
            rbc.rbc_all_news_href_business(n=2)
            rbc.rbc_get_posts()

        interfax = InterfaxParser(debug=True, url ='https://www.interfax.ru/business/')
        interfax.interfax_all_news_href_business(n=2)
        interfax.interfax_get_posts()

        to_csv()
        r = requests.get('127.0.0.1:5000/upload_csv') # запрос к NLP на скачку
        posts = get_all_posts()
        for post in posts:
            change_status(href = post.href, status=True)

    def polling(self):
        while True:
            rbc_urls = ['https://www.rbc.ru/economics/', 'https://www.rbc.ru/business/?utm_source=topline',
                        'https://www.rbc.ru/finances/?utm_source=topline',
                        'https://www.rbc.ru/politics/?utm_source=topline']
            for i in range(len(rbc_urls)):
                rbc = RBCParser(url=rbc_urls[i], debug=config['Debug']['debug'])
                rbc.rbc_all_news_href_business(n=2)
                rbc.rbc_get_posts()

            interfax = InterfaxParser(debug=config['Debug']['debug'], url='https://www.interfax.ru/business/')
            interfax.interfax_all_news_href_business(n=2)
            interfax.interfax_get_posts()
            unsend = unsend_posts()
            for post in unsend:
                r = requests.post('127.0.0.1:5000/post_handler', json={"title": post.title, "href": post.href,"text":post.text,"date_time":post.date_time,"source_site":post.source_site,"views":post.views}) #NLP
                change_status(href=post.href, status=True)
            time.sleep(5)



app = App()
app.first_start()
app.polling()



