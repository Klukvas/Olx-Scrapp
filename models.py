from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.dialects.mysql import TEXT

from settings import host_db, name_db, username_db,password_db

from Logging import Logger

Base = declarative_base()
log = Logger().custom_logger()
#?charset=utf8mb4
class DataBaseClient:
    def __init__(self):
        self.engine = create_engine(f'mysql+pymysql://{username_db}:{password_db}@{host_db}/{name_db}')
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            log.successfully('Database successfully created')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

class ModelRecord(Base):
    __tablename__ = 'Records'
    number_record = Column(String(100), primary_key=True, unique = True, index = True)
    record_categoty = Column(String(100))
    title = Column(String(100))
    price = Column(String(50))       
    description = Column(TEXT())       
    date_publish = Column(String(100))
    views = Column(String(100))
    name_user = Column(String(100))
    phone = Column(String(100))
    image_href = Column(String(100))
    record_url = Column(String(2000))
