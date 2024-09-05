from typing import Annotated
from fastapi import FastAPI

from ops import send_email

app = FastAPI()



@app.get('/')
def land():
    return {"msg": "welcome to the email server"}


@app.get('/send-email')
def send_mail(recipient_email: Annotated[str, None] = None):
    send_email(recipient_email)