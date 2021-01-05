from sqlalchemy import engine_from_config, Column, null, Integer, String, JSON, DateTime
from sqlalchemy.schema import Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Dict
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
    current_pubkey = Column(String)
    eff_date = Column(DateTime)
    exp_date = Column(DateTime)
    create_date = Column(DateTime)
    modify_date = Column(DateTime)

    def __init__(self, val_client_uuid: str,
                 val_department: str, val_sme_name: str,
                 val_current_pubkey: str,
                 val_eff_date: datetime, val_exp_date: datetime,
                 val_create_by: str, is_new_row: bool):
        self.client_uuid = val_client_uuid
        self.department = val_department
        self.sme_name = val_sme_name
        self.current_pubkey = val_current_pubkey
        self.eff_date = val_eff_date
        self.exp_date = val_exp_date
        if is_new_row:
            self.create_date = datetime.today()
        self.modify_date = datetime.today()


class ClientRepositoryOp(object):
    def __init__(self):
        engine = engine_from_config(config_client)
        # TODO: Find other parameter values for sessionmaker() to ensure proper DB operations.
        SessionClient = sessionmaker(bind=engine)
        self._session = SessionClient()
        BaseClient.metadata.create_all(engine)

    def write(self, val_client_uuid: str,
              val_department: str, val_sme_name: str,
              val_current_pubkey: str,
              val_eff_date: datetime, val_exp_date: datetime) -> None:
        try:
            new_row = ClientRepository(val_client_uuid,
                                       val_department, val_sme_name,
                                       val_current_pubkey,
                                       val_eff_date, val_exp_date, True)
            self._session.add(new_row)
            self._session.commit()
        except Exception as ex:
            print(ex)
            logging.error('ClientRepositoryOp write() error: ', sys.exc_info()[0])

    def update(self, val_client_uuid: str,
               val_department: str = None, val_sme_name: str = None,
               val_current_pubkey: str = None,
               val_eff_date: datetime = None, val_exp_date: datetime = None) -> None:
        try:
            update_row = self._session.query(ClientRepository)\
                .filter(ClientRepository.client_uuid == val_client_uuid)\
                .one()
            is_modified = False
            if val_department is not None:
                update_row.department = val_department
                is_modified = True
            if val_sme_name is not None:
                update_row.sme_name = val_sme_name
                is_modified = True
            if val_current_pubkey is not None:
                update_row.current_pubkey = val_current_pubkey
                is_modified = True
            if val_eff_date is not None:
                update_row.eff_date = val_eff_date
                is_modified = True
            if val_exp_date is not None:
                update_row.exp_date = val_exp_date
                is_modified = True
            if is_modified:
                self._session.commit()
        except Exception as ex:
            print(ex)
            logging.error('ClientRepositoryOp update() error: ', sys.exc_info()[0])

    def read(self, val_client_uuid: str) -> Dict:
        try:
            query_row = self._session.query(ClientRepository)\
                .filter(ClientRepository.client_uuid == val_client_uuid)\
                .one()
            return {'id': query_row.id,
                    'client_uuid': query_row.client_uuid,
                    'department': query_row.department,
                    'sme_name': query_row.sme_name,
                    'current_pubkey': query_row.current_pubkey,
                    'eff_date': query_row.eff_date,
                    'exp_date': query_row.exp_date,
                    'create_date': query_row.create_date,
                    'modify_date': query_row.modify_date}
        except Exception as ex:
            print(ex)
            logging.error('ClientRepositoryOp read() error: ', sys.exc_info()[0])

    def close(self) -> None:
        self._session.close()
