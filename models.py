from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, conint, constr, validator

class SurveySubmission(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    age: conint(ge=13, le=120)
    consent: bool
    rating: conint(ge=1, le=5)
    comments: Optional[constr(max_length=1000)] = None
    source: str = "other"

    # new fields used by app.py
    submission_id: Optional[str] = None
    user_agent: Optional[str] = None

    @validator("comments")
    def _trim(cls, v):
        return v.strip() if v else v

class StoredSurveyRecord(BaseModel):
    submission_id: str
    name: str
    email_hash: str
    age_hash: str
    consent: bool
    rating: int
    comments: Optional[str] = None
    source: str = "other"
    received_at: str
    ip: str = ""
    user_agent: Optional[str] = None
