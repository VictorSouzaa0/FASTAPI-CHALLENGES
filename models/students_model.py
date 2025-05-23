from core.config import settings
from sqlalchemy import Column, Integer, Boolean, Float, String, ForeignKey
from models.instructor_model import InstructorModel
class StudentModel(settings.DBBaseModel):
    __tablename__ = "student"

    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    name: str = Column(String(256))
    last_name: str = Column(String(256))
    age: int = Column(Integer())
    responsible_id: int = Column (Integer(ForeignKey('instructor.id')))
