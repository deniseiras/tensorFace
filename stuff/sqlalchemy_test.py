import sqlalchemy

from sqlalchemy import create_engine
engine = create_engine('sql:///:memory:', echo=True)