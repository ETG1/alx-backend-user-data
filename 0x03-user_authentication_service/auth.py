#!/usr/bin/env python3
"""
Auth module with password hashing
"""
import bcrypt


class Auth:
    """Auth class for user authentication services"""

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password with bcrypt and return the salted hash as bytes.
        This is a private method.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def hash_password(self, password: str) -> bytes:
        """
        Public method to hash a password.
        """
        return self._hash_password(password)
