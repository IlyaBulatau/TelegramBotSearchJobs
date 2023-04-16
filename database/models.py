from sqlalchemy import BigInteger, Integer, String, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger(), primary_key=True)
    requests = relationship('Request')
    page = relationship('Page', back_populates='user', uselist=False)

class Request(Base):
    __tablename__ = "requests"

    id = Column(String(90), primary_key=True)
    job = Column(String(90), nullable=False)
    sort = Column(String(10), nullable=False)
    page = Column(Integer(), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id'))
    user = relationship('User')
    reports = relationship('Report')

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer(), primary_key=True)
    title = Column(String(255))
    salary = Column(String(50))
    description = Column(String(1000))
    link = Column(String(255))
    request_id = Column(String(), ForeignKey('requests.id'))
    request = relationship('Request')

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer(), primary_key=True)
    current = Column(Integer(), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id'))
    user = relationship('User', back_populates='page', uselist=False)
