import configparser
from Parser import *

config = configparser.ConfigParser()
config.read("config.ini")


rbc = RBCParser(debug=config['Debug']['debug'])
rbc.rbc_all_news_href_business(n=1500)
rbc.rbc_get_posts()

interfax = InterfaxParser(debug=config['Debug']['debug'])
interfax.interfax_all_news_href_business(n=50)
interfax.interfax_get_posts()

