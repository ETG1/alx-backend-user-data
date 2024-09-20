#!/usr/bin/env python3
""" SessionDBAuth module for session authentication with persistence in the database (file)
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime
import models


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class for session management with database persistence
    """

    def create_session(self, user_id=None):
        """ Create and store a new session in the database (file)
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create a UserSession instance
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save the session in the file (database)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve the user_id for a given session ID from the database (file)
        """
        if session_id is None:
            return None

        # Search for the session in the database
        user_sessions = models.storage.all(UserSession)
        for session in user_sessions.values():
            if session.session_id == session_id:
                return session.user_id

        return None

    def destroy_session(self, request=None):
        """ Destroy the session by removing it from the database (file)
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Search for the session and delete it
        user_sessions = models.storage.all(UserSession)
        for session in user_sessions.values():
            if session.session_id == session_id:
                session.remove()  # Remove the session from the file (database)
                return True

        return False

