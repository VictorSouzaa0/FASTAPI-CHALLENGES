from typing import Optional

from pydantic import BaseModel as SCBaseModel

class InsctructorSchema(SCBaseModel):
    id: Optional[int] = None
    name: str
    last_name = str
    age = int
    image = str

    
    class Config:
        orm_mode = True
