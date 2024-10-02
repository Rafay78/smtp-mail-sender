import os
from typing import Annotated, Optional
from fastapi import File, UploadFile, Form, Depends, HTTPException, Body, Request, APIRouter
from ops import send_email
import shutil
from settings import settings
from googleapiclient.discovery import build
import base64 
import os.path 
from google.oauth2.credentials import Credentials 
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


router = APIRouter(
    tags=["Email Send Routes"]
)

land_router = APIRouter(
    tags=["Landing Page"]
)

@land_router.get('/')
def land():
    return {"msg": "welcome to the email server"}



@router.post("/send-email")
async def send_email(
                    message: Optional[str] = Form(None) , 
                    subject: Optional[str] = Form(None),
                    file: Optional[UploadFile] = File(None),
                    userInfo : Optional[UploadFile] = File(None)
                    ):
    
    user_info_data = await userInfo.read()
    data = json.loads(user_info_data.decode('utf-8'))
    html_content = f"<h1>{subject}</h1><p>{message}</p>"

    creds = Credentials(
        token=data['access_token'],
        refresh_token=data.get('refresh_token'),
        token_uri=data['token_uri'],
        client_id=data['client_id'],
        client_secret=data['client_secret']
    )

    try:
        service = build('gmail', 'v1', credentials=creds)

        # message_body = f"Hello, this is a test email from {data['name']} ({data['email']})."
                # mail_body = {
                    # 'raw': base64.urlsafe_b64encode(
                    #         f"From: {data['email']}\r\n"
                    #         f"To: t7827087@gmail.com\r\n"
                    #         f"Subject: Test Email from FastAPI\r\n\r\n"
                    #         f"{message_body}".encode('utf-8')
                    #     ).decode('utf-8')
                    # }


        if file :
            with open(f"./emails/{data['email']}.txt", "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file = open(f"./emails/{data['email']}.txt", 'r')
            for email_in_line in file:
                email_in_line = email_in_line.strip()
                if email_in_line:
                    msg = MIMEMultipart('alternative')
                    msg['From'] = f"{data['name']} <{data['email']}>"
                    msg['Subject'] = subject
                    
                    html_part = MIMEText(html_content, 'html')
                    msg.attach(html_part)
                    msg['To'] = email_in_line
                    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
                    mail_body = {'raw': raw_message}
                    send_message = service.users().messages().send(userId="me", body=mail_body).execute()
                    print(f"Email successfully sent to {email_in_line} from {data['email']}")
        return {"message": "Email sent successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
        return {"message": "Email sent failed!"}



@router.post('/send-mail')
def send_mail(recipient_email: Annotated[str, None] = None, message: Optional[str] = Form(None) ,subject: Optional[str] = Form(None), email: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    # if email :
    #     settings.sender_email = email
    print(subject)
    print(message)
    if file :
        with open(f"./emails.txt", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    send_email(recipient_email)

    
    # delete file when task done. 
    try:
        os.remove(f'./emails.txt')
        return {"message": "File processed and deleted successfully", "email": email, "filename": file.filename}
    except Exception as e:
        return {"message": f"Error deleting file: {str(e)}"}




@router.post("/upload")
async def upload_file(
    email: str = Form(...),   # Accept email as a Form field
    file: UploadFile = File(...)  # Accept file as a File upload
):
    with open(f"./email.txt", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_uploaded = open(f'./email.txt', 'r')
    for email_in_line in file_uploaded:
        print(email_in_line)
    
    try:
        os.remove(f'./email.txt')
        return {"message": "File processed and deleted successfully", "email": email, "filename": file.filename}
    except Exception as e:
        return {"message": f"Error deleting file: {str(e)}"}
        
    return {"success": "delivered"}