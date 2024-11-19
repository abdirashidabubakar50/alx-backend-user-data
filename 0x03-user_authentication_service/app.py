#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort,  make_response
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
    Handles the user login logic
    """
    email = request.form.get("email")
    password = request.form.get("pasword")

    # validate form inputs
    if not email or not password:
        abort(401, description="Invalid credentials")

    # create a session for the user
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
