from celery import shared_task, Celery
from time import sleep
from .models import UserData

app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

# app = Celery('simplejwt')
# @shared_task
# def send_Email(user_id):
#     user = UserData.objects.get(pk = user_id)

# @shared_task
# def clear_session_cache(id):
#     print(f"session cache cleared: {id}")
#     return id

# @shared_task()

@app.task
def reverse(text):
    print(f"reversing text: {text}")
    return text[::-1]