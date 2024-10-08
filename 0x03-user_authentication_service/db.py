#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import User, Base


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
        """ Add a new user. """
        if not email or not hashed_password:
            return None
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **attr) -> User:
        """ Search for a user by it attributes. """
        query = self._session.query(User)
        for key, value in attr.items():
            if hasattr(User, key):
                query = query.filter(getattr(User, key) == value)
            else:
                raise InvalidRequestError()

        user = query.first()
        if not user:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **attr) -> None:
        """ Updates a user in the users table. """
        if not user_id:
            return None

        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound()

        for key, value in attr.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                self._session.rollback()
                raise ValueError
        self._session.commit()
