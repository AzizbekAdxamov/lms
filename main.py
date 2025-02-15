from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from models import User, Branch, Group, Student  # SQLAlchemy modellari
from schemas import UserCreate, User, Branch, Group, Student, StudentCreate, GroupCreate  # Pydantic schemalar
from auth import get_current_user, create_access_token  # Auth funksiyalari
from typing import List

app = FastAPI()

# Ma'lumotlar bazasini yaratish
Base.metadata.create_all(bind=engine)

# OAuth2 autentifikatsiya
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Ma'lumotlar bazasiga ulanish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Role tekshirish funksiyasi
def check_role(current_user: User, required_role: str):
    if current_user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Faqat {required_role} uchun ruxsat berilgan",
        )

# SuperAdmin uchun endpointlar
@app.post("/admins", response_model=User)
def create_admin(admin: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "SuperAdmin")
    # SuperAdmin uchun Admin yaratish logikasi
    db_admin = User(username=admin.username, password_hash=admin.password, role="Admin", branch_id=admin.branch_id)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

@app.get("/branches", response_model=List[Branch])
def get_branches(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "SuperAdmin")
    # Barcha filiallarni ko'rish
    return db.query(Branch).all()

@app.get("/teachers", response_model=List[User])
def get_all_teachers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "SuperAdmin")
    # Barcha Teacherlarni ko'rish
    return db.query(User).filter(User.role == "Teacher").all()

@app.get("/groups", response_model=List[Group])
def get_all_groups(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "SuperAdmin")
    # Barcha guruhlarni ko'rish
    return db.query(Group).all()

@app.get("/students", response_model=List[Student])
def get_all_students(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "SuperAdmin")
    # Barcha studentlarni ko'rish
    return db.query(Student).all()

# Admin uchun endpointlar
@app.post("/teachers", response_model=User)
def create_teacher(teacher: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "Admin")
    # O'z filialidagi Teacher yaratish logikasi
    db_teacher = User(username=teacher.username, password_hash=teacher.password, role="Teacher", branch_id=current_user.branch_id)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@app.post("/students", response_model=Student)
def create_student(student: StudentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "Admin")
    # O'z filialidagi Student yaratish logikasi
    db_student = Student(name=student.name, group_id=student.group_id, branch_id=current_user.branch_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.post("/groups", response_model=Group)
def create_group(group: GroupCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "Admin")
    # O'z filialidagi Group yaratish logikasi
    db_group = Group(name=group.name, teacher_id=group.teacher_id, branch_id=current_user.branch_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@app.get("/teachers", response_model=List[User])
def get_teachers(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "Admin")
    # O'z filialidagi Teacherlarni ko'rish
    return db.query(User).filter(User.role == "Teacher", User.branch_id == current_user.branch_id).all()

@app.get("/students", response_model=List[Student])
def get_students(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "Admin")
    # O'z filialidagi Studentlarni ko'rish
    return db.query(Student).filter(Student.branch_id == current_user.branch_id).all()

@app.get("/groups", response_model=List[Group])
def get_groups(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "Admin")
    # O'z filialidagi guruhlarni ko'rish
    return db.query(Group).filter(Group.branch_id == current_user.branch_id).all()

# Teacher uchun endpointlar
@app.get("/my-groups", response_model=List[Group])
def get_my_groups(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "Teacher")
    # O'z guruhlarini ko'rish
    return db.query(Group).filter(Group.teacher_id == current_user.id).all()

@app.get("/my-students", response_model=List[Student])
def get_my_students(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_role(current_user, "Teacher")
    # O'z guruhidagi Studentlarni ko'rish
    return db.query(Student).filter(Student.group_id.in_(
        [group.id for group in current_user.groups]
    )).all()

# Ishga tushirish
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)