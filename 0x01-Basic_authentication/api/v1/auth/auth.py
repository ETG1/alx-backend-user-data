#!/usr/bin/env python3
"""
Module for authentication
"""

from typing import List, Optional
from flask import request

class Auth:
    """Base class for authentication methods.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a path requires authentication based on excluded paths.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths or patterns that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        # Check for exact matches and wildcard matches
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                # If excluded_path ends with '*', it should match any path that starts with the same prefix
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """Retrieves the Authorization header from the request.

        Args:
            request (Flask request object, optional): The request object.

        Returns:
            Optional[str]: The Authorization header or None if not present.
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """Retrieves the User instance for a request.

        Args:
            request (Flask request object, optional): The request object.

        Returns:
            Optional[TypeVar('User')]: The User instance if authentication is successful, otherwise None.
        """
        return None

