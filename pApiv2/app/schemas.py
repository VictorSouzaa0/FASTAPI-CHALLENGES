from pydantic import BaseModel
from typing import Optional

class InstructorBase(BaseModel):
    nome: str
    idade: int
    turma_atuacao: str
    image: Optional[bytes] = None 

class InstructorCreate(InstructorBase):
    pass

class Instructor(InstructorBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    nome: str
    idade: int
    image: Optional[bytes] = None 
    instructor_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    
    class Config:
        from_attributes = True