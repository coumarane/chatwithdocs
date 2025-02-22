from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm

class OAuth2PasswordRequestFormEmail(OAuth2PasswordRequestForm):
    def __init__(self, email: str = Form(...), password: str = Form(...)):
        super().__init__(username=email, password=password)
        self.email = email
