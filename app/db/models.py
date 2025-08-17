from sqlalchemy import Column,Text, Integer, String, ForeignKey, Date, DateTime, Enum, JSON, Float, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    

    