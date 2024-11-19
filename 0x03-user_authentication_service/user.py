#!/usr/bin/env python3

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
""" This model defines a model User
"""
Base = declarative_base()


class User(Base):
    """ Model User, defines database table users
    """
    __tablename__ = 'users'

    id = Column(Integer,  primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
