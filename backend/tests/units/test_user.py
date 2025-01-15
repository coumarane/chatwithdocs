import pytest
from app.domain import User

users = [
    {
        "username": "coumar",
        "email": "coumar@example.com",
        "password": "pass123"
    },
    {
        "username": "helios",
        "email": "helios@example.com",
        "password": "pass123"
    }
]

def test_create_user():
    user = {
        "username": "helios",
        "email": "helios@example.com",
        "password": "pass123"
    }
