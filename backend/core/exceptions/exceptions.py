from fastapi import HTTPException, status

class BaseException(Exception):
    """This is the base class for all exceptions"""
    pass

class UserEmailAlreadyExistsException(BaseException):
    """User email already exists"""
    pass