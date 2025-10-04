from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text,
    Date, DateTime, Enum, JSON, Float, Boolean,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    level = Column(String)
    total_chapters = Column(Integer)
    duration = Column(Integer)

    chapters = relationship(
        "Chapter",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True)
    chapter_number = Column(Integer)
    title = Column(String)
    description = Column(Text)
    estimated_duration = Column(Integer)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))

    course = relationship(
        "Course",
        back_populates="chapters",
        passive_deletes=True
    )

    sections = relationship(
        "Section",
        back_populates="chapter",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    content = Column(Text)
    language = Column(String, nullable=True)
    explanation = Column(Text, nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"))

    chapter = relationship(
        "Chapter",
        back_populates="sections",
        passive_deletes=True
    )

class Otp(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, index=True)
    otp = Column(String(6), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

