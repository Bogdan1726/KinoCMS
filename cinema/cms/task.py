from math import floor
from time import sleep
from cinema.celery import app
from django.core.mail import send_mail
from celery import shared_task
from celery_progress.backend import ProgressRecorder


# @app.task
# def my_task(users_list):
#     user_email = users_list
#     send_mail('Test',
#               'Test Celery Django Task',
#               'okcdnipro@gmail.com',
#               user_email,
#               fail_silently=False)

# Celery Task
@shared_task(bind=True)
def process_download(self, users_list):
    print('Task started')
    progress_recorder = ProgressRecorder(self)
    print('Start')
    count = len(users_list)
    result = 0
    for email in users_list:
        sleep(1)
        result += 1
        prog = floor((result/count)*100)
        print(f"{prog}-%")
        # Update progress on the web page
        progress_recorder.set_progress(prog, 100)
    print('End')

    return 'Task Complete'
