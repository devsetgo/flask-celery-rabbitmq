from flask import Flask
from cel_example import make_celery
from flask_sqlalchemy import SQLAlchemy
import requests
import time
from random import choice
from dotenv import load_dotenv
import os

load_dotenv()
FAKERESPONSE_KEY = os.getenv("FAKERESPONSE_KEY")


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest:guest@localhost:32771'
app.config['CELERY_BACKEND'] = 'db+sqlite:///results.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'

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
    url = f'http://www.fakeresponse.com/api/?sleep=5&api_key={FAKERESPONSE_KEY}'

    # st = []
    for i in range(0,60):
        r = requests.get(url)
        data = str(r.json())
        result = Results(data=data)
        db.session.add(result)
    
    db.session.commit()
    return 'done'

@app.route('/insert-data')
def insertData():
    x = f'async request sent at {time.time()}'
    # insert.delay()
    api_call.delay()
    return x

@celery.task(name='run.insert')
def insert():
    url = f'http://www.fakeresponse.com/api/?sleep=1&api_key={FAKERESPONSE_KEY}'

    for i in range(1000):
        data =''.join(choice('ABCDE') for i in range(10))
        result = Results(data=data)
        db.session.add(result)
    
    db.session.commit()
    return 'done'



if __name__ == '__main__':
    app.run(debug=True)