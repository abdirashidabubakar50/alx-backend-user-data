#!/usr/bin/env python3
""" A class BasicAuth that inherits from the class Auth
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ class BasicAuth inherits from Auth
    """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """ Returns the authorization header value after Basic
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if authorization_header and authorization_header.startswith("Basic "):
            return authorization_header[len("Basic "):]
        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """ decodes teh authorization header file as UTF-8 string
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header, validate=True
            )
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, ValueError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Extracts the user email and password
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
            ':', 1)
        return user_email, user_password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ Returns User instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})

        if not users:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance based on the request's authorization
        """

        # Retrieve the authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # extract the base64 authorization part
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        # decode the Base64 authorization part
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None

        # extract user credentials
        email, password = self.extract_user_credentials(decoded_auth)

        if email is None or password is None:
            return None

        # Retrieve the User instance based on credentials
        return self.user_object_from_credentials(email, password)
