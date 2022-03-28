from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from dotenv import dotenv_values
import jwt
from typing import List

from starlette.responses import JSONResponse

from models import User

config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASSWORD"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(email: List, instance: User):
    token_data = {
        "id": instance.id,
        "username": instance.username
    }

    token = jwt.encode(token_data, config_credentials['SECRET'], algorithm='HS256')

    template = f"""
        <!doctype html>
        <html>
            <head>
                
            </head>
            <body>
                <div style="display: flex; align-items: center; justify-content: center; flex-direction: column">
                    <h3>
                        Account Verification
                    </h3>
                    <br />
                    <p>Thanks for registering with us. click the link bellow to verify your account</p>
                    <a style="margin-top: 1rem; padding: 1rem; 
                        border-radius: 0.5rem; font-size: 1rem; 
                        text-decoration: none; background: purple, color: white;"
                        href="http://localhost:8000/verication/?token={token}">
                        Verify email
                    </a>
                </div>
            </body>
        </html>
    """
    message = MessageSchema(
        subject="ACCOUNT VERIFICATION",
        recipients=email,
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
