from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app import models, schemas
from app.database import AsyncSessionLocal, engine, Base

app = FastAPI()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/instructors/", response_model=schemas.Instructor)
async def create_instructor(instructor: schemas.InstructorCreate, db: AsyncSession = Depends(get_db)):
    db_instructor = models.Instructor(**instructor.dict())
    db.add(db_instructor)
    await db.commit()
    await db.refresh(db_instructor)
    return db_instructor

@app.get("/instructors/", response_model=List[schemas.Instructor])
async def read_instructors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Instructor).offset(skip).limit(limit))
    instructors = result.scalars().all()
    return instructors

@app.get("/instructors/{instructor_id}", response_model=schemas.Instructor)
async def read_instructor(instructor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Instructor).where(models.Instructor.id == instructor_id))
    instructor = result.scalars().first()
    if instructor is None:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@app.put("/instructors/{instructor_id}", response_model=schemas.Instructor)
async def update_instructor(
    instructor_id: int, 
    instructor: schemas.InstructorCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Instructor).where(models.Instructor.id == instructor_id))
    db_instructor = result.scalars().first()
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    for key, value in instructor.dict().items():
        setattr(db_instructor, key, value)
    
    await db.commit()
    await db.refresh(db_instructor)
    return db_instructor

@app.delete("/instructors/{instructor_id}")
async def delete_instructor(instructor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Instructor).where(models.Instructor.id == instructor_id))
    db_instructor = result.scalars().first()
    if db_instructor is None:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    await db.delete(db_instructor)
    await db.commit()
    return {"message": "Instructor deleted successfully"}

@app.post("/students/", response_model=schemas.Student)
async def create_student(student: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[schemas.Student])
async def read_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).offset(skip).limit(limit))
    students = result.scalars().all()
    return students

@app.get("/students/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    student = result.scalars().first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.Student)
async def update_student(
    student_id: int,
    student: schemas.StudentCreate, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    db_student = result.scalars().first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    
    await db.commit()
    await db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.id == student_id))
    db_student = result.scalars().first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    await db.delete(db_student)
    await db.commit()
    return {"message": "Student deleted successfully"}

@app.get("/instructors/{instructor_id}/students/", response_model=List[schemas.Student])
async def read_students_by_instructor(instructor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Student).where(models.Student.instructor_id == instructor_id)
    )
    students = result.scalars().all()
    return students