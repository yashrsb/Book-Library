from celery import Celery

c_app = Celery()

c_app.config_from_object('src.config')

@c_app.task()
def send_mail():
        message = create_message(
        recipients=[email], subject="Verify your email", body=html_message
    )
    bg_tasks.add_task(mail.send_message,message)