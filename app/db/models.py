from sqlalchemy import Column,Text, Integer, String, ForeignKey, Date, DateTime, Enum, JSON, Float, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    level = Column(String)
    total_chapters = Column(Integer)
    duration = Column(Integer)

    chapters = relationship("Chapter", back_populates="course")

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True)
    chapter_number = Column(Integer)
    title = Column(String)
    description = Column(Text)
    estimated_duration = Column(Integer)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="chapters")
    sections = relationship("Section", back_populates="chapter")

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    content = Column(Text)
    language = Column(String, nullable=True)
    explanation = Column(Text, nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))

    chapter = relationship("Chapter", back_populates="sections")
