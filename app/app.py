from fastapi import FastAPI, HTTPException, status
from app.model.requests.template import TemplateRequest, TemplateResponse
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