"""
Utilities for creating / querying an SQLite database.

Note: Shortcut used by SQLite DB. Given more time I would create a
standalone database(MySQL / Postgres) in a separate container to
allow the database to be persisted between runs AND to allow multiple
flask processes to access it at once.

Shortcut:
    - Didn't use a a Database migration tool (Alembic)
    - Skipped Testing
"""
import os
import sqlite3
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE = 'demo.db'


def init_db():
    """ Creates / Overwrites local SQLite database with required schema"""
    with open(os.path.join('sql', 'schema.sql'), mode='r') as f:
        db = sqlite3.connect(DATABASE)
        db.cursor().executescript(f.read())
        db.commit()


# Note: Old cookie cutter code from SQLAlchemy documentation
# https://stackoverflow.com/questions/14799189/avoiding-boilerplate-session-handling-code-in-sqlalchemy-functions
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    engine = create_engine(f'sqlite:///{DATABASE}')

    session = sessionmaker(engine)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
