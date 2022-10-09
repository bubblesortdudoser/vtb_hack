import os
from database.dbworker import rewrite_title_post

from config import app
from flask_cors import cross_origin
from flask import request, jsonify, send_from_directory

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

if __name__ == '__main__':
    app.run(threaded=True, port=5000)