import configparser
from Parser import *

config = configparser.ConfigParser()
config.read("config.ini")

parser = InterfaxParser(debug=config['Debug']['debug'])
parser.interfax_all_news_href_business()