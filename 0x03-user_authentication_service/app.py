#!/usr/bin/env python3
"""
Flask app for user authentication and session management.
Provides endpoints for user registration, login, logout, 
profile access, and password reset functionality.
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth  # Importing the Auth class for authentication logic

AUTH = Auth()  # Initialize the Auth class instance for user handling

app = Flask(__name__)  # Initialize the Flask app

@app.route('/', methods=['GET'])
def index() -> str:
    """
    GET /
    Root endpoint that returns a welcome message.
    Returns:
        JSON response: {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    POST /users
    Register a new user with email and password.
    If the email is already registered, it returns a 400 error.

    Form Data:
        - email: User's email (string)
        - password: User's password (string)
    
    Returns:
        JSON response with user's email and success message or error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Attempt to register a user. Catch exception if the user already exists.
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    POST /sessions
    Log in a user by validating the email and password.
    Creates a session and sets a session_id cookie if valid.

    Form Data:
        - email: User's email (string)
        - password: User's password (string)
    
    Returns:
        JSON response indicating login success and sets session cookie.
        If login is invalid, returns a 401 error.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if login credentials are valid
    if not (AUTH.valid_login(email, password)):
        abort(401)  # Abort with 401 Unauthorized if login fails
    else:
        # Create a session and set the session_id as a cookie
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    DELETE /sessions
    Log out the user by destroying their session.
    Requires a valid session_id cookie.

    Returns:
        Redirects to the root endpoint if logout is successful.
        If no valid session is found, returns a 403 error.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)  # Abort with 403 Forbidden if session is invalid
    AUTH.destroy_session(user.id)  # Destroy the user's session
    return redirect('/')  # Redirect to the home page after logout


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    GET /profile
    Retrieve the user's profile using the session_id cookie.

    Returns:
        JSON response with the user's email if session is valid.
        If no valid session is found, returns a 403 error.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)  # Abort with 403 Forbidden if session is invalid


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Generates a reset password token for the user.

    Form Data:
        - email: User's email (string)
    
    Returns:
        JSON response with the reset token if email is valid.
        If email is not found, returns a 403 error.
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)  # Abort with 403 Forbidden if email is invalid


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """
    PUT /reset_password
    Updates the user's password using a valid reset token.

    Form Data:
        - email: User's email (string)
        - reset_token: Password reset token (string)
        - new_password: New password (string)

    Returns:
        JSON response confirming password update.
        If the token or other data is invalid, returns a 403 error.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)  # Abort with 403 Forbidden if reset token is invalid


if __name__ == "__main__":
    # Run the Flask app on 0.0.0.0:5000 for external access
    app.run(host="0.0.0.0", port="5000")
