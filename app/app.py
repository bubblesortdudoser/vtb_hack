import configparser
from Parser import *

config = configparser.ConfigParser()
config.read("config.ini")

parser = Parser(debug=config['Debug']['debug'])
parser.interfax_all_news_business()