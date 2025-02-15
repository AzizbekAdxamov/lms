from sqlalchemy import Column, Integer, String, ForeignKey, Enum  # Enum ni import qiling
from sqlalchemy.orm import relationship
from database import Base

# ENUM turini yaratish
from enum import Enum as PyEnum

class RoleEnum(str, PyEnum):
    SUPERADMIN = "SuperAdmin"
    ADMIN = "Admin"
    TEACHER = "Teacher"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum, name="role_enum"))  # ENUM uchun nom ko'rsatish
    branch_id = Column(Integer, ForeignKey("branches.id"))
    branch = relationship("Branch")
    groups = relationship("Group", back_populates="teacher")  # Teacherning guruhlari

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    branch_id = Column(Integer, ForeignKey("branches.id"))
    teacher = relationship("User", back_populates="groups")  # Teacher bilan bog'lanish
    branch = relationship("Branch")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))
    branch_id = Column(Integer, ForeignKey("branches.id"))
    group = relationship("Group")
    branch = relationship("Branch")