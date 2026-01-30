from pydantic import BaseModel
from typing import Optional

class FactCheckRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
