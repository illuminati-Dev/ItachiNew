from sys import exit as exiter

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from SaitamaRobot import DB_URI, LOGGER


def start() -> scoped_session:
    engine = create_engine(DB_URI,
                           client_encoding="utf8",
                           pool_recycle=3600,
                           pool_pre_ping=True)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    LOGGER.info("Established connection to PSQL Database!")
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
try:
    SESSION: scoped_session = start()
except SQLAlchemyError as e:
    LOGGER.error(f"Error in PSQL: {e}")
    exiter(1)
LOGGER.info("Initialized PSQL-Database!")
