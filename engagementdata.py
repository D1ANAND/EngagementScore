from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# In-memory database 
database = {}

class CreateModelRequest(BaseModel):
    modelId: str
    ContractAddress: str

@app.post("/create")
async def create_model(request: CreateModelRequest):
    if request.modelId in database:
        raise HTTPException(status_code=400, detail="Model ID already exists")
    database[request.modelId] = {
        "ContractAddress": request.ContractAddress,
        "EngagementScore": 0
    }
    return {"message": "Model created successfully"}


class UpdateModelRequest(BaseModel):
    modelId: str

@app.post("/update")
async def update_model(request: UpdateModelRequest):
    if request.modelId not in database:
        raise HTTPException(status_code=404, detail="Model ID not found")
    database[request.modelId]["EngagementScore"] += 1
    return {"message": "Engagement score updated successfully"}


class ViewModelResponse(BaseModel):
    modelId: str
    EngagementScore: int


@app.get("/view/{modelId}", response_model=ViewModelResponse)
async def view_model(modelId: str):
    if modelId not in database:
        raise HTTPException(status_code=404, detail="Model ID not found")
    return ViewModelResponse(
        modelId=modelId,
        EngagementScore=database[modelId]["EngagementScore"]
    )


if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app)
    uvicorn.run(app,port=int(os.environ.get('PORT', 8080)), host="0.0.0.0")