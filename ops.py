from fastapi import HTTPException
from settings import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Annotated, Union




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