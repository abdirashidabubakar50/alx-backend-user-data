#!/usr/bin/env python3
""" Defines the auth class to authenticate the user
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """ Hashes a password with bcrypt using a generated salt.
        Args:
            password (str): The password string to has

        Returns:
            bytes: The salted hash of the password
        """

        # ensure the password is in bytes
        password_bytes = password.encode('utf-8')

        # Generate a salt
        salt = bcrypt.gensalt()

        # Hash the password using the salt
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user with the provided email and password

        Args:
            email (str): The user's email address
            password (str): THe user's plain-text password

        Returns:
            User: The newly created user object

        Raises:
            ValueError: if a user already exists with given email
        """

        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            pass

        hashed_password = self._hash_password(password)

        new_user = self._db.add_user(email, hashed_password)

        return new_user

    def valid_login(self, email: str, password: str):
        """ Validate a user login by checking the provided email and password
        """
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except Exception:
            return False


def _generate_uuid() -> str:
    """ Generate a new UUID and return its string representaion
    This is a private method and should not be used outsied this module

    Returns:
        str: A string representaion of a new UUID.
    """
    return str(uuid.uuid4())
