from sqlalchemy import (
    create_engine, Date, String, Integer, SmallInteger, Column, Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import (
    DBMS,
    DBUSER,
    DBPASS,
    DBHOST,
    DBPORT,
    DBNAME,
    TABLENAME
)

DeclarativeBase = declarative_base()


def db_connect(dbms=None, dbuser=None, dbpass=None, dbhost='localhost', dbport=None, dbname=None):
    """
    Performs database connection using database settings.
    if settings is not specified, return sqlite instance
    Returns sqlalchemy engine instance
    """
    if all((dbuser, dbpass, dbhost, dbport, dbname)):
        return create_engine(f'{dbms}://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}')
    return create_engine(f'sqlite:///db/{TABLENAME}.db')


def create_table(engine):
    """
    Create table, specified by engine
    """
    DeclarativeBase.metadata.create_all(engine)


class Results(DeclarativeBase):
    """SQLAlchemy model"""
    
    __tablename__ = TABLENAME
    
    id = Column(Integer, primary_key=True)
    url = Column('url', String(120))
    team1 = Column('team1', String(20))
    score1 = Column('score1', SmallInteger)
    team2 = Column('team2', String(20))
    score2 = Column('score2', SmallInteger)
    winner = Column('winner', String(20))
    maps = Column('maps', String(5))
    stars = Column('stars', SmallInteger)
    date = Column('date', Date)
    event = Column('event', String(50))


class HltvPipeline(object):
    
    def __init__(self):
        """Create table"""
        engine = db_connect(DBMS, DBUSER, DBPASS,
                            DBHOST, DBPORT, DBNAME
        )
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
    
    def process_item(self, item, spider):
        """Insert rows into table"""
        session = self.Session()
        db = Results(**item)

        try:
            session.add(db)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
