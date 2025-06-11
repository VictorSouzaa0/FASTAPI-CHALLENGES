from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from app.database import Base

class Instructor(Base):
    __tablename__ = "instructors"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    turma_atuacao = Column(String)
    image = Column(LargeBinary)
    
    alunos = relationship("Student", back_populates="instructor")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    image = Column(LargeBinary)
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    
    instructor = relationship("Instructor", back_populates="alunos")