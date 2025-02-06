The fastapi use the package aiosmtplib to send an email
https://aiosmtplib.readthedocs.io/en/stable/index.html
To mock the smtp server in local we use docker image mailhog.

How Run Server Mail MailHog

# Installation

1. Make the script executable:
```bash
chmod +x install_mailhog.sh
```

2. Run the script:
```bash
./install_mailhog.sh
```

# Test
Launch backend api and execute the following command in terminal:
```bash
curl -X POST "http://localhost:8000/send-email" \
-H "Content-Type: application/json" \
-d '{
      "to_email": "c.coumarane@gmail.com",
      "subject": "Test Email",
      "body": "This is a test email from FastAPI."
    }'
```
