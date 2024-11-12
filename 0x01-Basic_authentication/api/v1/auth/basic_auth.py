#!/usr/bin/env python3
""" A class BasicAuth that inherits from the class Auth
"""
from api.v1.auth.auth import Auth


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
