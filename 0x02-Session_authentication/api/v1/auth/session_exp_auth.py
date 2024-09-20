#!/usr/bin/env python3
""" Module for Session Expiration Authentication
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Expiration Authentication class
    """

    def __init__(self):
        """ Initialize the session expiration authentication
        """
        session_duration = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a new session and store the session info with expiration
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session data including creation time
        session_data = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve the user ID for a given session ID and check for expiration
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        if "created_at" not in session_data:
            return None

        created_at = session_data.get("created_at")
        if self.session_duration <= 0:
            return session_data.get("user_id")

        # Check if the session has expired
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_data.get("user_id")

