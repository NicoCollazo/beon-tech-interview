from pydantic import BaseModel, Field

class InterviewRequest(BaseModel):
    prompt: str = Field(..., description="The interview question or prompt", min_length=1)

class InterviewResponse(BaseModel):
    answer: str