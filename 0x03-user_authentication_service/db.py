#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User  # Import the Base and User classes


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session  # Get the current session
        session.add(new_user)  # Add the new user to the session
        session.commit()  # Commit the transaction to save the user
        return new_user  # Return the newly created User object

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The first user found that matches the filters.

        Raises:
            NoResultFound: If no user is found with the given filters.
            InvalidRequestError: If invalid query arguments are passed.
        """
        session = self._session  # Get the current session
        try:
            # Attempt to get exactly one result
            return session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the specified parameters")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments passed")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing
            the attributes to update.

        Raises:
            ValueError: If any attribute in kwargs is not
            a valid attribute of the User model.
        """
        session = self._session  # Get the current session
        try:
            user = self.find_user_by(id=user_id)  # Locate the user by id
        except NoResultFound:
            raise ValueError(f"User with id {user_id} does not exist")

        # Update attributes if they exist on the User model
        for key, value in kwargs.items():
            if hasattr(user, key):
                # Set the new balue for the attribute
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

        session.commit()  # Commit the changes to the database
