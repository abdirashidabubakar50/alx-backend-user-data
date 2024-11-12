#!/usr/bin/env python3
"""
Module that defines class to manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Manages API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method return False - Now
        """
        return False

    def authorization_header(self, request=None) -> str:
        """public method returnds None - request(Flask Object)
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ public method that returns None - request(Flask request object)
        """
        return None
