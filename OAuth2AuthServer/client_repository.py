from sqlalchemy import create_engine, Column, null, Integer, String, JSON, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
import logging
import sys

BaseClient = declarative_base()
BaseCredential = declarative_base()
config_client = {
    'sqlalchemy.url': 'sqlite:///client_repo.db',
    'sqlalchemy.echo': False
    }
config_credential = {
    'sqlalchemy.url': 'sqlite:///credential_repo.db',
    'sqlalchemy.echo': False
    }


class ClientRepository(BaseClient):
    __tablename__ = 'client_repository'
    id = Column(Integer, primary_key=True)
    client_uuid = Column(String(50))
    department = Column(String(50))
    sme_name = Column(String(50))
    eff_date = Column(DateTime)
    exp_date = Column(DateTime)
    create_date = Column(DateTime)
    create_by = Column(String(50))


class CredentialRepository(BaseCredential):
    __tablename__ = 'credential_repository'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    private_key = Column(String)
    public_key = Column(String)
    eff_date = Column(DateTime)
    exp_date = Column(DateTime)
    create_date = Column(DateTime)
    create_by = Column(String(50))


class ClientRepositoryOp:
    def __init__(self):
        _engine = create_engine('sqlite:///tic-tac-toe.db', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(self.engine)


    def write(self, the_state, the_winner):
        try:
            game_data = GameState(the_state, the_winner)
            self.session.add(game_data)
            self.session.commit()
        except:
            logging.error('TicTacToeDbOp write() error: ', sys.exc_info()[0])
        return

    def close(self):
        self.session.close()


class GameState(Base):
    __tablename__ = 'game_state'
    id = Column(Integer, primary_key=True)
    # state = Column(JSON)
    state = Column(String)
    winner = Column(String(1))
    create_datetime = Column(DateTime)

    def __init__(self, the_state, the_winner):
        self.state = the_state
        self.winner = the_winner
        self.create_datetime = date.today()