import os
from typing import Annotated, Optional
from fastapi import FastAPI, File, UploadFile, Form
from fastapi import APIRouter
from ops import send_email
import shutil

from settings import settings



router = APIRouter(
    tags=["Email Send Routes"]
)

@router.get('/')
def land():
    return {"msg": "welcome to the email server"}


@router.post('/send-email')
def send_mail(recipient_email: Annotated[str, None] = None, email: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    # if email :
    #     settings.sender_email = email
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