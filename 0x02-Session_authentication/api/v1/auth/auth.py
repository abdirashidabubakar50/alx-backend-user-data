#!/usr/bin/env python3
"""
Module that defines class to manage API authentication
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """ Manages API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method return False - Now
        """

        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        normalized_path = path if path.endswith('/') else path + '/'

        if normalized_path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """public method returnds None - request(Flask Object)
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ public method that returns None - request(Flask request object)
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME", "_my_session_id")

        return request.cookies.get(session_name)
