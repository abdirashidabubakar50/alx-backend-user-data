#!/usr/bin/env python3
""" Defines the auth class to authenticate the user
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

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

        hashed_password = _hash_password(password)

        new_user = self._db.add_user(email, hashed_password)

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
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

    def create_session(self, email: str) -> str:
        """ Creates a session ID for a user with the given email

        Args:
            email(str): the email of the user

        Returns:
            str: the newly created session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str):
        """ Retrieve a user by their session id
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ updates the corresponding user's session ID to None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """ updates the user's reset_token database field

        Args:
            email (str): the user's email

        Returns:
            str : user's new reset_token
        """
        try:
            user = self._db.find_user_by(email=email)

        except NoResultFound:
            raise ValueError("user does not exist")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates the user's password using reset token"""

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError("user does not exist")

        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None
        )


def _hash_password(password: str) -> bytes:

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


def _generate_uuid() -> str:
    """ Generate a new UUID and return its string representaion
    This is a private method and should not be used outsied this module

    Returns:
        str: A string representaion of a new UUID.
    """
    return str(uuid.uuid4())
