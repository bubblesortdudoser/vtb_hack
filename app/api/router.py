import os
import wget

from config import app
from flask_cors import cross_origin
from flask import request, jsonify, send_from_directory

from database.dbworker import rewrite_title_post

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, '../csv/')

@app.route('/api/rewrite_title', methods=['POST'])
@cross_origin(supports_credentials=True)
def rewrite_title():
    title = request.json['title']
    href = request.json['href']

    rewrite_title_post(title=title,href=href)

    return jsonify(ping = "OK!")

@app.route('/api/csv/<path:filename>', methods=['GET'])
@cross_origin(supports_credentials=True)
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'data.csv', as_attachment=True)

########################
@app.route('/post_handler', methods=['POST'])
def post_handler():
    title = request.json['title']
    href = request.json['href']
    text = request.json['text']
    date_time = request.json['date_time']
    source_site = request.json['source_site']
    views = request.json['views']
    print('ok')
    return jsonify(status = "200")

@app.route('/upload_csv', methods=['POST'])
def handler():
    wget.download('127.0.0.1:5000/api/csv/data.csv')

    return jsonify(status = "200")

if __name__ == '__main__':
    app.run(threaded=True, port=5000)