
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from media.s3_storage import S3MediaStorage
import os
import boto3
import json

#class FilePhotoStack:
    #def add_pending_photo(self, target_name) 
#otworz plik, dopisz do pliku, zamknij plik



class InMemoryPhotoStack:
    def __init__(self):
       self.photos_list = []
    def get_all_photos(self):
       return self.photos_list
    def add_pending_photo(self, target_name):
       self.photos_list.append(target_name) 
s3 = boto3.resource('s3')
storage = S3MediaStorage(s3, os.getenv('APP_BUCKET_NAME'))
app = Flask(__name__)
photo_stack = InMemoryPhotoStack()
sqs = boto3.resource('sqs', region_name="eu-central-1")
pending_orders = sqs.get_queue_by_name(QueueName='JUSTYNAsQUEUE')

@app.route("/")
def hello():
    return render_template('upload_form.html')

@app.route("/upload", methods=['POST'])
def make_upload():
    if 'filetoupload' not in request.files:
      return 'fail'
    myfile = request.files['filetoupload']
    target_name = "uploads/%s"%myfile.filename
    storage.store(dest=target_name, source=myfile)
    photo_stack.add_pending_photo(target_name)
    return 'ok'

@app.route("/order")
def order():
    return render_template('order.html', photos=photo_stack.get_all_photos())

@app.route("/proceed", methods=['POST'])
def proceed():
    order_ani_request = {'email': request.form['email'], 'photos': photo_stack.get_all_photos()}
    pending_orders.send_message(MessageBody=json.dumps(order_ani_request))

    return redirect(url_for('order'))

@app.route("/list")
def list():
    mydata=[{"name": "Jakub"}, {"name": "Justyna"}]
    return render_template('peoples.html', peoples=mydata)
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080, debug=True)

