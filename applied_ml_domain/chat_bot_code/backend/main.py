from fastapi import FastAPI
from pydantic import BaseModel
from retrival_pipeline import retrieve
from fastapi.middleware.cors import CORSMiddleware

class Query(BaseModel):
    query:str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/query")
async def retrieve_answer(query_request : Query):
    query = query_request.query
    response = retrieve(query)
    print(query)
    print(response)
    return response
    