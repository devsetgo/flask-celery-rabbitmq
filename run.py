from flask import Flask
from cel_example import make_celery
from flask_sqlalchemy import SQLAlchemy
import requests
import time
import datetime
from random import choice
from dotenv import load_dotenv
import os
import json

load_dotenv()
FAKERESPONSE_KEY = os.getenv("FAKERESPONSE_KEY")


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.getenv("CELERY_BROKER_URL")
app.config['CELERY_BACKEND'] = os.getenv("CELERY_BACKEND")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

celery = make_celery(app)
db = SQLAlchemy(app)
db.create_all()

class Results(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.String(4000))
    

@app.route('/')
def index():

    template = 'index.html'
    return 'Hi'

@app.route('/process/<name>')
def process_name(name):
    reverse.delay(name)
    # api_call.delay()
    return 'sent an async request'

@celery.task(name='run.reverse')
def reverse(your_name):
    time.sleep(5)
    return your_name[::-1]


@celery.task(name='run.api_call')
def api_call():
    url = f'http://www.fakeresponse.com/api/?sleep=1&api_key={FAKERESPONSE_KEY}'

    response_json = []
    # st = []
    for i in range(0,5):
        r = requests.get(url)
        # data = str(r.json())
        # result = Results(data=data)
        # db.session.add(result)
        response_json.append(r.json())
    
    # db.session.commit()
    save_json(response_json)
    
    return 'done'

def save_json(data):
    file_path = (os.path.abspath("data/data.json"))
    with open(file_path, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)

    return "done"

def open_json():
    file_path = (os.path.abspath("data/data.json"))
    print(file_path)
    with open(file_path) as jsonfile:
        data = json.load(jsonfile)
    
    return data


@app.route('/insert-data')
def insertData():
    now = datetime.datetime.now().strftime('%Y %B %d %H:%M:%S')
    x = f'async request sent at {now}.'
    # insert.delay()
    api_call.delay()
    return x

@app.route('/view-data')
def viewData():
    data = open_json()
    text = str(data)
    return text

if __name__ == '__main__':
    app.run(debug=True)