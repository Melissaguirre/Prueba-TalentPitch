from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()


class Flow(Base):
    __tablename__ = "flows"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime)
    views = Column(Integer)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    slug = Column(String)
    phone = Column(String)
    country = Column(String)
    city = Column(String)
    gender = Column(String)
    birth_date = Column(DateTime)
    created_at = Column(DateTime)


class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    slug = Column(String)
    video = Column(String)
    views = Column(Integer)
    level_experience = Column(String)
    status = Column(String)
    role_name = Column(String)
    skills = Column(String)
    created_at = Column(DateTime)


class ResumeExhibited(Base):
    __tablename__ = "resumes_exhibited"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    model_id = Column(Integer, ForeignKey("flows.id"))
    model_type = Column(String)
    sent_at = Column(DateTime)
    created_at = Column(DateTime)


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("flows.id"))
    model_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    value = Column(Integer)
    created_at = Column(DateTime)


class Share(Base):
    __tablename__ = "shares"
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("flows.id"))
    model_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)


class View(Base):
    __tablename__ = "views"
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("flows.id"))
    model_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    created_at = Column(DateTime)


class Profile(Base):
    __tablename__ = "profiles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    skills = Column(String)
    tools = Column(String)
    languages = Column(String)
    dream_brands = Column(String)
    dream_roles = Column(String)
    areas_of_interest = Column(String)
