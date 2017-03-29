# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy_utils import ChoiceType

import autocloud

Base = declarative_base()


class JobDetails(Base):
    __tablename__ = 'job_details'

    STATUS_TYPES = (
        ('s', 'Success'),
        ('f', 'Failed'),
        ('a', 'Aborted'),
        ('r', 'Running'),
        ('q', 'Queued')
    )

    IMAGE_FAMILY_TYPES = (
        ('b', 'Base'),
        ('a', 'Atomic')
    )

    ARCH_TYPES = (
        ('i386', 'i386'),
        ('x86_64', 'x86_64')
    )

    id = Column(Integer, primary_key=True)
    taskid = Column(String(255), nullable=False)
    status = Column(ChoiceType(STATUS_TYPES))
    family = Column(ChoiceType(IMAGE_FAMILY_TYPES))
    arch = Column(ChoiceType(ARCH_TYPES))
    release = Column(String(255))
    output = Column(Text, nullable=False, default='')
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    user = Column(String(255), nullable=False)


class ComposeDetails(Base):
    __tablename__ = 'compose_details'

    STATUS_TYPES = (
        ('c', 'Complete'),
        ('q', 'Queued'),
        ('r', 'Running'),
    )
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    compose_id = Column(String(255), nullable=False, unique=True)
    respin = Column(Integer, nullable=False)
    type = Column(String(255), nullable=False)
    passed = Column(Integer, nullable=True, default=0)
    failed = Column(Integer, nullable=True, default=0)
    status = Column(ChoiceType(STATUS_TYPES))
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    location = Column(String(255), nullable=False)


class ComposeJobDetails(Base):
    __tablename__ = 'compose_job_details'

    STATUS_TYPES = (
        ('s', 'Success'),
        ('f', 'Failed'),
        ('a', 'Aborted'),
        ('r', 'Running'),
        ('q', 'Queued')
    )

    IMAGE_FAMILY_TYPES = (
        ('b', u'Base'),
        ('a', u'Atomic')
    )

    ARCH_TYPES = (
        ('i386', 'i386'),
        ('x86_64', 'x86_64')
    )

    id = Column(Integer, primary_key=True)
    arch = Column(ChoiceType(ARCH_TYPES))
    compose_id = Column(String(255), nullable=False)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    family = Column(ChoiceType(IMAGE_FAMILY_TYPES))
    image_url = Column(String(255), nullable=False)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    output = Column(Text, nullable=False, default='')
    release = Column(String(255))
    status = Column(ChoiceType(STATUS_TYPES))
    subvariant = Column(String(255), nullable=False)
    user = Column(String(255), nullable=False)
    image_format = Column(String(255), nullable=False)
    image_type = Column(String(255), nullable=False)
    image_name = Column(String(255), nullable=False)


def create_tables():
    # Create an engine that stores data in the local directory
    engine = create_engine(autocloud.SQLALCHEMY_URI)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)


def init_model():
    engine = create_engine(autocloud.SQLALCHEMY_URI)
    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession
