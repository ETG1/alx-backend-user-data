#!/usr/bin/env python3
"""
Test script for the Flask app endpoints using requests.
"""
import requests

BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Registers a new user with the provided email and password.
    Asserts the status code and response payload.
    """
    response = requests.post(f"{BASE_URL}/users", data={'email': email,
                                                        'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempts to log in with the wrong password.
    Asserts that the status code is 401 (Unauthorized).
    """
    response = requests.post(f"{BASE_URL}/sessions", data={'email': email,
                                                           'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Logs in with the correct credentials.
    Asserts that the status code is 200 and returns the session_id from cookies.
    """
    response = requests.post(f"{BASE_URL}/sessions", data={'email': email,
                                                           'password': password})
    assert response.status_code == 200
    assert "session_id" in response.cookies
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Tries to access the profile endpoint without being logged in.
    Asserts that the status code is 403 (Forbidden).
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Accesses the profile endpoint while logged in using the provided session_id.
    Asserts the status code is 200 and the correct email is returned.
    """
    cookies = {'session_id': session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Logs out the user by deleting the session.
    Asserts that the status code is 200 and a redirect occurs.
    """
    cookies = {'session_id': session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Requests a reset password token for the given email.
    Asserts the status code is 200 and the reset token is returned.
    """
    response = requests.post(f"{BASE_URL}/reset_password", data={'email': email})
    assert response.status_code == 200
    assert "reset_token" in response.json()
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Updates the user's password using the reset token.
    Asserts the status code is 200 and the password is updated.
    """
    response = requests.put(f"{BASE_URL}/reset_password", data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


# Test data
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
