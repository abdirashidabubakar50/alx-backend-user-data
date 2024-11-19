#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import Base
from user import User


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

    def add_user(self, email: str,  hashed_password: str) -> User:
        """ adds a user to the database
        
        Args:
            email: the email of the user
            hashed_password: hashed password of the uer
         
         Returns:
            user: returns the User instance of the added user
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ finds a user by arbitrary keyword arguments
        """
        if not kwargs:
            raise InvalidRequestError("No arguments provided for filtering")

        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found with the given criteria")
            return user

        except AttributeError:
            raise InvalidRequestError("Invalid query arguments provided.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user's information based on user_id and keyword
        arguments

        Args:
            user_id (int): The ID of the user to update
            **kwargs: Arbitrary keyword arguments representing user
            attributes to update

        Raises:
            ValueError: If an invalid attribute is passed
        """
        user = self.find_user_by(id=user_id)

        valid_user_attributes = ['email', 'hashed_password', 'session_id', 'reset_token']

        for key, value in kwargs.items():
            if key not in valid_user_attributes:
                raise ValueError(f"Invalid attribute: {key}")

            setattr(user, key, value)

        self._session.commit()
