#!/usr/bin/env python3
""" A class BasicAuth that inherits from the class Auth
"""
from api.v1.auth.auth import Auth
import base64


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
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
            ':', 1)
        return user_email, user_password
