# smtp-mail-sender

It can send emails in batch for your business

### Steps to setup the Application

Installation steps:

### Firstly, you will need the `client_secret.json` file for this project to make it functional.

1. Clone the repository:

   ```bash
   git clone https://github.com/Rafay78/smtp-mail-sender.git
   ```

2. Navigate into the project directory:

   ```bash
   cd smtp-mail-sender
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a file named `.env` & Set up environment variables in it:

   ```bash
   SENDER_EMAIL="xyz@gmail.com"
   EMAIL_PASSWORD="712365"
   SMTP_SERVER_NAME="Smtp.gmail.com"
   DATABASE_HOSTNAME="localhost"
   ```

5. Start the application:
   ```bash
   uvicorn main:app --reload
   ```

# Before Sending the Email Request (!Important)

    Make sure you set Allow less secure apps to On, in your google account settings. This is how you can do that:

    1. Click manage your Google account on your account icon (on top right corner).

    2. Activate 2 factor Authentication.

    3. Search for Apps Password. It will prompt you to add a name of the password. (It will only show the password once make sure to copy properly.)

    4. Add the generated and copied password to the env variable in the EMAIL_PASSWORD variable.

# Add the recipient list

you must add the recipient emails list in the `emails.txt` file.

# Edit the html Email Message

You can customize the email message in the `email_template.html`.

Navigate to your browser to access the fastApi docs swagger documentation:

```
localhost:8000/docs
```

Execute the request, hurrah you just did it.
