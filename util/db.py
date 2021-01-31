import sqlalchemy as db
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import (
	Column, 
	Integer,
	String,
	Binary,
	ForeignKey,
	DateTime,
	Bool
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Source(Base):
	__tablename__ = 'sources'
	id = Column(Integer, primary_key=True)
	source_url = Column(String, nullable=False)
	page_selector = Column(String)
	# the number of minutes between update checks. 0 to disable, -1 to always check
	update_frequency = Column(Integer)
	description = Column(String)
	last_checked = Column(DateTime)# nullable for first creation?

class RawData(Base):
	__tablename__ = 'raw_data'
	id = Column(Integer, primary_key=True)
	source_id = Column(None, ForeignKey('sources.id'))
	data_format = Column(String)
	raw_data = Column(Binary)
	filename = Column(String)
	hash = Column(Binary)
	date_created = Column(DateTime)


# set up DB
engine = db.create_engine('sqlite:///covid-datasources.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
