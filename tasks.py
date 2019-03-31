from celery import Celery
import requests


result_backend = 'db+sqlite:///results.db'

app = Celery('tasks', broker='amqp://guest:guest@1localhost:5672', backend=result_backend)

# your_name = 'backwards'

@app.task
def reverse(your_name):
        
    return your_name[::-1]

@app.task
def api_call():
    url = f'http://www.fakeresponse.com/api/?sleep=1&api_key={FAKERESPONSE_KEY}'

    st = []
    for i in range(0,10):
        r = requests.get(url)
        st.append(r.json)
    
    return st
