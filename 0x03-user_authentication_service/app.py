#!/usr/bin/env python3
"""
app.py

This module implements a user authentication service using Flask.
It includes routes for user registration, login, and session management.
"""

from flask import Flask, jsonify, request, abort,  make_response, redirect
from auth import Auth

# initialize the Flask app
app = Flask(__name__)
AUTH = Auth()


# Define the route for the home page
@app.route("/", methods=["GET"])
def home():
    """ GET '/'
    route for homepage"""
    # return a JSON response
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """ POST '/users'
     Handles the  user registration logic
    """
    # get the email and password from form data
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """ POST '/sessions'
    Handles user login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # validate form inputs
    # if not email or password:
    #     abort(401, description="Email and password must be provided")

    # Authenticate user
    if not AUTH.valid_login(email, password):
        abort(401, description="Invalid credentials.")

    # create session for the user
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=['DELETE'])
def logout():
    """ Handles the DELETE /sessions route to logout a user

    if the session ID exists, destroy the session and redirect to GET /.
    Otherwise, respond with 403 HTTP status
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """ Handles the GET /profile route
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """ Handles password reset request route POST /reset_password
    """
    email = request.form.get('email')

    if not email:
        abort(400, description="email is required")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403, description="email not registered")


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """ Handles password reset requests.

    Request form data:
     - email : The user's email address
     - reset_token: The reset token for password reset_token
     - new_password: the new password to reset

    Returns:
        - 200 HTTP response iwth a success message if password updated
        = 403 HTTP responce if the reset token is invalid or any other error"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(403, description='Missing email, reset_token or new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403, description='Invalid reset token')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
