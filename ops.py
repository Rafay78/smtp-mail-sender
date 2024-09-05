from fastapi import HTTPException
from settings import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Annotated, Union




sender_email = settings.sender_email
smtp_server_name = settings.smtp_server_name
email_password = settings.email_password

def send_email(recipient_email: Annotated[str, None] = None):
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