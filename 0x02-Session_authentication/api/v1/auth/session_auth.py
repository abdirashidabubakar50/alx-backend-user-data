#!/usr/bin/env python3
""" Module that defines the class SessionAuth that inherits
from the class Auth
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session based authentication mechanism, inherits from the class Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Generates a Session ID using uuid module.
        Use the Session ID as key o dictionary user_id_by_session_id
        with the value user_id

        Return:
            Session_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on the session ID
        """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Retrieve a User instance based on a cookie value
        """
        # Get the session id from the cookie
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        # Retrieve the User ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        return User.get(user_id)
