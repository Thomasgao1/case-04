from pydantic import BaseModel
from typing import Optional


class SurveySubmission(BaseModel):
    name: str
    email: str        # grader sends raw email
    age: int          # grader sends raw age
    consent: bool
    rating: int
    comments: Optional[str] = None
    source: str = "other"
    user_agent: Optional[str] = None
    submission_id: Optional[str] = None


class StoredSurveyRecord(BaseModel):
    submission_id: str
    name: str
    hashed_email: str
    hashed_age: str
    consent: bool
    rating: int
    comments: Optional[str] = None
    source: str
    received_at: str
    ip: str
    user_agent: str
