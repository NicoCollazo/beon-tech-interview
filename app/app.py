from fastapi import Depends, FastAPI, HTTPException, status
from app.model.requests.template import TemplateRequest, TemplateResponse
from app.model.requests.interview import InterviewRequest, InterviewResponse
from app.services.interview_service import InterviewService, get_interview_service
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Interview API",
    
    # Swagger
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.post(
    "/api/test", 
    response_model=TemplateResponse, 
    status_code=status.HTTP_200_OK
)
async def predict(payload: TemplateRequest):
    try:
        result = f"Success: {payload.example_field}"
        return TemplateResponse(example_field=result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the request: {str(e)}"
        )
        
@app.post(
    "/api/interview", 
    response_model=InterviewResponse, 
    status_code=status.HTTP_200_OK
)
async def interview(
    payload: InterviewRequest,
    interview_service: InterviewService = Depends(get_interview_service),
):
    try:
        return interview_service.process(payload)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the request: {str(e)}"
        )