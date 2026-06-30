from pydantic import BaseModel, Field

class TemplateRequest(BaseModel):
    example_field: str = Field(..., description="Example field", min_length=1)

class TemplateResponse(BaseModel):
    example_field: str