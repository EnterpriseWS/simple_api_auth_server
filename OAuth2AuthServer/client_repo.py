from sqlalchemy import engine_from_config, Column, null, Integer, String, JSON, DateTime
from sqlalchemy.schema import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
import logging
import sys

BaseClient = declarative_base()
config_client = {
    'sqlalchemy.url': 'sqlite:///client_repo.db',
    'sqlalchemy.echo': False
    }


class ClientRepository(BaseClient):
    __tablename__ = 'client_repository'
    id = Column(Integer,
                Sequence('article_aid_seq', start=1238, increment=1),
                # sqlite_autoincrement=True,
                primary_key=True)
    client_uuid = Column(String(50))
    department = Column(String(50))
    sme_name = Column(String(50))
    eff_date = Column(DateTime)
    exp_date = Column(DateTime)
    create_by = Column(String(50))
    create_date = Column(DateTime)

    def __init__(self, val_client_uuid,
                 val_department, val_sme_name,
                 val_eff_date, val_exp_date,
                 val_create_by):
        self.client_uuid = val_client_uuid
        self.department = val_department
        self.sme_name = val_sme_name
        self.eff_date = val_eff_date
        self.exp_date = val_exp_date
        self.create_by = val_create_by
        self.create_date = date.today()


class ClientRepositoryOp:
    def __init__(self):
        engine = engine_from_config(config_client)
        # TODO: Find other parameter values for sessionmake() to ensure proper DB operations.
        SessionClient = sessionmaker(bind=engine)
        self._session = SessionClient()
        BaseClient.metadata.create_all(engine)

    def write(self, val_client_uuid,
              val_department, val_sme_name,
              val_eff_date, val_exp_date,
              val_create_by):
        try:
            new_row = ClientRepository(val_client_uuid,
                                       val_department, val_sme_name,
                                       val_eff_date, val_exp_date,
                                       val_create_by)
            self._session.add(new_row)
            self._session.commit()
        except Exception as ex:
            print(ex)
            logging.error('ClientRepositoryOp write() error: ', sys.exc_info()[0])
        return

    def close(self):
        self._session.close()
