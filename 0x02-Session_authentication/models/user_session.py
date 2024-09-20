#!/usr/bin/env python3
""" UserSession module for managing session in the database (file)
"""
from models.base import Base
import models


class UserSession(Base):
    """ UserSession class to manage session data in a file
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a new UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

