
from flask import Flask
from flask import render_template
from flask import request
from media.s3_storage import S3MediaStorage
import os
import boto3

s3 = boto3.resource('s3')
storage = S3MediaStorage(s3, os.getenv('APP_BUCKET_NAME'))
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('upload_form.html')

@app.route("/upload", methods=['POST'])
def make_upload():
    if 'filetoupload' not in request.files:
      return 'fail'
    myfile = request.files['filetoupload']
    storage.store(dest="uploads/%s"%myfile.filename, source=myfile)
    return 'ok'

@app.route("/list")
def list():
    mydata=[{"name": "Jakub"}, {"name": "Justyna"}]
    return render_template('peoples.html', peoples=mydata)
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080, debug=True)
