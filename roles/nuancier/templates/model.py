# -*- coding: utf-8 -*-
#
# Copyright © 2013  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

'''
Mapping of python classes to Database Tables.
'''

__requires__ = ['SQLAlchemy >= 0.7', 'jinja2 >= 2.4']
import pkg_resources

import datetime
import logging

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relation
from sqlalchemy.orm import backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm.collections import mapped_collection
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import and_
from sqlalchemy.sql.expression import Executable, ClauseElement

BASE = declarative_base()

error_log = logging.getLogger('nuancier.lib.model')


def create_tables(db_url, alembic_ini=None, debug=False):
    """ Create the tables in the database using the information from the
    url obtained.

    :arg db_url, URL used to connect to the database. The URL contains
        information with regards to the database engine, the host to
        connect to, the user and password and the database name.
          ie: <engine>://<user>:<password>@<host>/<dbname>
    :kwarg alembic_ini, path to the alembic ini file. This is necessary
        to be able to use alembic correctly, but not for the unit-tests.
    :kwarg debug, a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a session that can be used to query the database.

    """
    engine = create_engine(db_url, echo=debug)
    BASE.metadata.create_all(engine)

    if alembic_ini is not None:  # pragma: no cover
        # then, load the Alembic configuration and generate the
        # version table, "stamping" it with the most recent rev:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(alembic_ini)
        command.stamp(alembic_cfg, "head")

    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


class Elections(BASE):
    '''This table lists all the elections available.

    Table -- Elections
    '''

    __tablename__ = 'Elections'
    id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    election_name = sa.Column(sa.String(255), nullable=False, unique=True)
    election_folder = sa.Column(sa.String(50), nullable=False, unique=True)
    election_year = sa.Column(sa.Integer, nullable=False)
    election_open = sa.Column(sa.Boolean, nullable=False, default=False)
    election_public = sa.Column(sa.Boolean, nullable=False, default=False)
    election_n_choice = sa.Column(sa.Integer, nullable=False)
    election_badge_link = sa.Column(sa.String(255), default=None)

    date_created = sa.Column(sa.DateTime, nullable=False,
                             default=sa.func.current_timestamp())
    date_updated = sa.Column(sa.DateTime, nullable=False,
                             default=sa.func.current_timestamp(),
                             onupdate=sa.func.current_timestamp())

    def __init__(self, election_name, election_folder, election_year,
                 election_open=False, election_public=False,
                 election_n_choice=16, election_badge_link=None):
        """ Constructor.

        :arg election_name:
        :arg election_folder:
        :arg election_year:
        :arg election_open:
        :arg election_public:
        :arg election_n_choice:
        :arg election_badge_link:
        """
        self.election_name = election_name
        self.election_folder = election_folder
        self.election_year = election_year
        self.election_open = election_open
        self.election_public = election_public
        self.election_n_choice = election_n_choice
        self.election_badge_link = election_badge_link

    def __repr__(self):
        return 'Elections(id:%r, name:%r, year:%r)' % (
            self.id, self.election_name, self.election_year)

    def api_repr(self, version):
        """ Used by fedmsg to serialize Elections in messages. """
        if version == 1:
            return dict(
                id=self.id,
                name=self.election_name,
                year=self.election_year,
            )
        else:  # pragma: no cover
            raise NotImplementedError("Unsupported version %r" % version)

    @classmethod
    def all(cls, session):
        """ Return all the entries in the elections table.
        """
        return session.query(
            cls
        ).order_by(
            Elections.election_year.desc()
        ).all()

    @classmethod
    def by_id(cls, session, election_id):
        """ Return the election corresponding to the provided identifier.
        """
        return session.query(cls).get(election_id)

    @classmethod
    def get_open(cls, session):
        """ Return all the election open.
        """
        return session.query(
            cls
        ).filter(
            Elections.election_open == True
        ).order_by(
            Elections.election_year.desc()
        ).all()

    @classmethod
    def get_public(cls, session):
        """ Return all the election public.
        """
        return session.query(
            cls
        ).filter(
            Elections.election_public == True
        ).order_by(
            Elections.election_year.desc()
        ).all()


class Candidates(BASE):
    ''' This table lists the candidates for the elections.

    Table -- Candidates
    '''

    __tablename__ = 'Candidates'
    id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    candidate_file = sa.Column(sa.String(255), nullable=False)
    candidate_name = sa.Column(sa.String(255), nullable=False)
    candidate_author = sa.Column(sa.String(255), nullable=False)
    election_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('Elections.id',
                      ondelete='CASCADE',
                      onupdate='CASCADE'
                      ),
        nullable=False,
    )

    date_created = sa.Column(sa.DateTime, nullable=False,
                             default=sa.func.current_timestamp())
    date_updated = sa.Column(sa.DateTime, nullable=False,
                             default=sa.func.current_timestamp(),
                             onupdate=sa.func.current_timestamp())

    election = relation('Elections')
    __table_args__ = (
        sa.UniqueConstraint('election_id', 'candidate_file'),
        sa.UniqueConstraint('election_id', 'candidate_name'),
    )

    def __init__(self, candidate_file, candidate_name, candidate_author,
                 election_id):
        """ Constructor

        :arg candidate_file: the file name of the candidate
        :arg candidate_name: the name of the candidate
        :arg candidate_author: the name of the author of this candidate
        :arg election_id: the identifier of the election this candidate is
            candidate for.
        """
        self.candidate_file = candidate_file
        self.candidate_name = candidate_name
        self.candidate_author = candidate_author
        self.election_id = election_id

    def __repr__(self):
        return 'Candidates(file:%r, name:%r, election_id:%r, created:%r' % (
            self.candidate_file, self.candidate_name, self.election_id,
            self.date_created)

    def api_repr(self, version):
        """ Used by fedmsg to serialize Packages in messages. """
        if version == 1:
            return dict(
                name=self.candidate_name,
                election=self.election.election_name,
            )
        else:  # pragma: no cover
            raise NotImplementedError("Unsupported version %r" % version)

    @classmethod
    def by_id(cls, session, candidate_id):
        """ Return the election corresponding to the provided identifier.
        """
        return session.query(cls).get(candidate_id)

    @classmethod
    def by_election(cls, session, election_id):
        """ Return the candidate associated to the given election
        identifier.

        """
        return session.query(cls).filter(
            Candidates.election_id == election_id).all()

    @classmethod
    def get_results(cls, session, election_id):
        """ Return the candidate of a given election ranked by the number
        of vote each received.

        """
        query = session.query(
            Candidates,
            sa.func.count(Votes.candidate_id).label('votes')
        ).filter(
            Candidates.election_id == election_id
        ).filter(
            Candidates.id == Votes.candidate_id
        ).group_by(
            Candidates.id
        ).order_by(
            'votes DESC'
        )
        return query.all()


class Votes(BASE):
    ''' This table lists the results of the elections

    Table -- Votes
    '''

    __tablename__ = 'Votes'
    user_name = sa.Column(sa.String(50), nullable=False, primary_key=True)
    candidate_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('Candidates.id',
                      onupdate='CASCADE'
                      ),
        nullable=False,
        primary_key=True
    )

    date_created = sa.Column(sa.DateTime, nullable=False,
                             default=sa.func.current_timestamp())
    date_updated = sa.Column(sa.DateTime, nullable=False,
                             default=sa.func.current_timestamp(),
                             onupdate=sa.func.current_timestamp())

    def __init__(self, user_name, candidate_id):
        """ Constructor

        :arg name: the name of the user who voted
        :arg candidate_id: the identifier of the candidate that the user
            voted for.
        """
        self.user_name = user_name
        self.candidate_id = candidate_id

    def __repr__(self):
        return 'Votes(name:%r, candidate_id:%r, created:%r' % (
            self.user_name, self.candidate_id, self.date_created)

    @classmethod
    def cnt_votes(cls, session, election_id,):
        """ Return the votes on the specified election.

        :arg session:
        :arg election_id:
        """
        return session.query(
            cls
        ).filter(
            Votes.candidate_id == Candidates.id
        ).filter(
            Candidates.election_id == election_id
        ).count()

    @classmethod
    def cnt_voters(cls, session, election_id,):
        """ Return the votes on the specified election.

        :arg session:
        :arg election_id:
        """
        return session.query(
            sa.func.distinct(cls.user_name)
        ).filter(
            Votes.candidate_id == Candidates.id
        ).filter(
            Candidates.election_id == election_id
        ).count()

    @classmethod
    def by_election(cls, session, election_id):
        """ Return the votes on the specified election.

        :arg session:
        :arg election_id:
        """
        return session.query(
            cls
        ).filter(
            Votes.candidate_id == Candidates.id
        ).filter(
            Candidates.election_id == election_id
        ).all()

    @classmethod
    def by_election_user(cls, session, election_id, username):
        """ Return the votes the specified user casted on the specified
        election.

        :arg session:
        :arg election_id:
        :arg username:
        """
        return session.query(
            cls
        ).filter(
            Votes.candidate_id == Candidates.id
        ).filter(
            Candidates.election_id == election_id
        ).filter(
            Votes.user_name == username
        ).all()
