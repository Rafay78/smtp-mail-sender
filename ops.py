from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from settings import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Annotated, Union
import models
import schema
from db import get_db
import base64 
import os.path 
from google.auth.transport.requests import Request 
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://mail.google.com/']
USER_TOKENS = 'token.json'

CREDENTIALS = 'C:\YouTube\dev\credentials.json'

def getToken() -> str:
    creds = None
    if os.path.exists(USER_TOKENS):
        creds = Credentials.from_authorized_user_file(USER_TOKENS, SCOPES)
        creds.refresh(Request())
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(USER_TOKENS, 'w') as token:
                token.write(creds.to_json())
                return creds.token




sender_email = settings.sender_email
smtp_server_name = settings.smtp_server_name
email_password = settings.email_password

def get_smtp_server(email):  
    smtp_servers = {  
        "gmail.com": "smtp.gmail.com",  
        "outlook.com": "smtp.live.com",  
        "hotmail.com": "smtp.live.com",  
        "office365.com": "smtp.office365.com",  
        "yahoo.com": "smtp.mail.yahoo.com",  
        "yahoo.co.uk": "smtp.mail.yahoo.co.uk",  
        "ntlworld.com": "smtp.ntlworld.com",  
        "btconnect.com": "smtp.btconnect.com",  
        "btopenworld.com": "mail.btopenworld.com",  
        "btinternet.com": "mail.btinternet.com",  
        "orange.net": "smtp.orange.net",  
        "orange.co.uk": "smtp.orange.co.uk",  
        "wanadoo.co.uk": "smtp.wanadoo.co.uk",  
        "comcast.net": "smtp.comcast.net",  
        "verizon.net": "outgoing.verizon.net",  
        "zoho.com": "smtp.zoho.com",  
        "mail.com": "smtp.mail.com",  
        "gmx.com": "smtp.gmx.com",  
        "o2.ie": "smtp.o2.ie",  
        "o2.co.uk": "smtp.o2.co.uk",  
        "att.yahoo.com": "smtp.att.yahoo.com",  
        "1and1.com": "smtp.1and1.com",  
        "1und1.de": "smtp.1und1.de",  
        "t-online.de": "securesmtp.t-online.de"  
    }  
    
    # Extract the domain from the email  
    domain = email.split('@')[-1]  
    
    # Return the corresponding SMTP server or None if not found  
    return smtp_servers.get(domain, None)  

# Example usage  
# email = "rafay@outlook.com"  
# smtp_server = get_smtp_server(email)  
# print(smtp_server)  # Output: smtp.gmail.com

def get_or_create_user(user: schema.User, db: Session):
    existing_user = db.query(models.Users).filter_by(email=user.email).first()
    if existing_user:
        return existing_user

    new_user = models.Users(name=user.name, email=user.email, image_url=str(user.picture))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def send_email(recipient_email: Annotated[str, None] = None,):

    # Read the HTML message from file
    with open('email_template.html', 'r') as file:
        html_content = file.read()


    # Step 1: Create SMTP object using host and port
    try:
        server = smtplib.SMTP(smtp_server_name, 587)

        # Step 2: Send EHLO to identify the client to the server
        ehlo_return = server.ehlo()
        print(f"ehlo retruned: {ehlo_return}")
        
        # Step 3: Start TLS connection
        tls_returned =server.starttls()
        print(f"TLS Handshaking: {tls_returned}")

        # Step 4: Login using email and password
        server.login(sender_email, email_password)

        if recipient_email:
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['Subject'] = 'Welcome to CloudConda'
            
            # Attach the HTML message to the real message
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            msg['To'] = recipient_email

            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"status: Email sent successfully to {recipient_email}!")
        else:    

            file = open('emails.txt', 'r')
            for email_in_line in file:
                # Step 5-9: Create message object and convert HTML to a proper email message
                msg = MIMEMultipart('alternative')
                msg['From'] = sender_email
                msg['Subject'] = 'Welcome to CloudConda'
                
                # Attach the HTML message to the real message
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
                msg['To'] = email_in_line

                # Step 10: Send the email
                server.sendmail(sender_email, email_in_line, msg.as_string())
                print(f"status: Email sent successfully to {email_in_line}!")

        # Step 11: Quit the SMTP connection
        server.quit()

        return {"status": "Email sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")