from typing import Optional

from pydantic import BaseModel as SCBaseModel


class StudentSchema(SCBaseModel):
    id: Optional[int] = None
    name: str
    last_name: str
    age: int
    responsible_id: int