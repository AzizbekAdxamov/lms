from pydantic import BaseModel
from typing import List, Optional

# User uchun Pydantic schema
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    branch_id: int

class User(UserBase):
    id: int
    role: str
    branch_id: int

    class Config:
        from_attributes = True  # SQLAlchemy modelini Pydantic modeliga aylantirish uchun

# Branch uchun Pydantic schema
class BranchBase(BaseModel):
    name: str

class Branch(BranchBase):
    id: int

    class Config:
        from_attributes = True

# Group uchun Pydantic schema
class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    teacher_id: int

class Group(GroupBase):
    id: int
    teacher_id: int
    branch_id: int

    class Config:
        from_attributes = True

# Student uchun Pydantic schema
class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    group_id: int

class Student(StudentBase):
    id: int
    group_id: int
    branch_id: int

    class Config:
        from_attributes = True