#!/usr/bin/env python3
"""Session Authentication Views
This module defines the routes related to session-based authentication.

Routes:
    POST /auth_session/login: Logs in a user based on email and password,
                              creates a session, and sets a session cookie.

Handles errors such as missing email, missing password, incorrect email,
incorrect password, and user not found.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """POST /auth_session/login
    Handles user login with Session Authentication.
    """

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user_list = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user_list or len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_list[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    # create session ID
    session_id = auth.create_session(user.id)
    if not session_id:
        return jsongy({"error": "could not create session"}), 500

    session_name = os.getenv('SESSION_NAME', 'session_id')
    # set session ID in the response cookies
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response, 200
