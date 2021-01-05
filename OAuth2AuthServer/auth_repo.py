from sqlalchemy import engine_from_config, Column, null, Integer, String, JSON, DateTime
from sqlalchemy.schema import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from typing import Dict
import logging
import sys

BaseAuth = declarative_base()
config_auth = {
    'sqlalchemy.url': 'sqlite:///auth_repo.db',
    'sqlalchemy.echo': False
    }


class AuthRepository(BaseAuth):
    __tablename__ = 'auth_repository'
    id = Column(Integer,
                Sequence('article_aid_seq', start=1001, increment=1),
                # sqlite_autoincrement=True,
                primary_key=True)
    client_id = Column(Integer)
    private_key = Column(String)
    public_key = Column(String)
    eff_date = Column(DateTime)
    exp_date = Column(DateTime)
    create_by = Column(String(50))
    create_date = Column(DateTime)

    def __init__(self, val_client_id,
                 val_private_key, val_public_key,
                 val_eff_date, val_exp_date,
                 val_create_by):
        self.client_id = val_client_id
        self.private_key = val_private_key
        self.public_key = val_public_key
        self.eff_date = val_eff_date
        self.exp_date = val_exp_date
        self.create_by = val_create_by
        self.create_date = date.today()


class AuthRepositoryOp:
    def __init__(self):
        engine = engine_from_config(config_auth)
        # TODO: Find other parameter values for sessionmaker() to ensure proper DB operations.
        SessionClient = sessionmaker(bind=engine)
        self._session = SessionClient()
        BaseAuth.metadata.create_all(engine)

    def write(self, val_client_id,
              val_private_key, val_public_key,
              val_eff_date, val_exp_date,
              val_create_by) -> None:
        try:
            new_row = AuthRepository(val_client_id,
                                     val_private_key, val_public_key,
                                     val_eff_date, val_exp_date,
                                     val_create_by)
            self._session.add(new_row)
            self._session.commit()
        except Exception as ex:
            print(ex)
            logging.error('AuthRepositoryOp write() error: ', sys.exc_info()[0])

    def read(self, val_client_id: int) -> Dict:
        try:
            query_row = self._session.query(AuthRepository)\
                .filter(AuthRepository.client_id == val_client_id)\
                .one()
            return {'id': query_row.id,
                    'client_id': query_row.client_id,
                    'private_key': query_row.private_key,
                    'public_key': query_row.public_key,
                    'eff_date': query_row.eff_date,
                    'exp_date': query_row.exp_date,
                    'create_by': query_row.create_by,
                    'create_date': query_row.create_date}
        except Exception as ex:
            print(ex)
            logging.error('ClientRepositoryOp read() error: ', sys.exc_info()[0])

    def close(self) -> None:
        self._session.close()
