import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)
config = load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DB_URL_postgres = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER,
        pw=POSTGRES_PW,
        url=POSTGRES_URL,
        db=POSTGRES_DB
)