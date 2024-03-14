from fastapi import FastAPI, HTTPException
from langserve import add_routes
from agent_components.tools_agent import Agent
from fastapi.responses import RedirectResponse 
from pydantic import BaseModel 
from fastapi.responses import JSONResponse 


app = FastAPI(
    title="LLM for SQL Demo",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)
agent = Agent()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

class Input(BaseModel):
    """sample questions:
        "hello" : for general context
        "How much is the cash amount on the invoice?" : for RAG based context
        "write SQL query to show the number of transactions in the table" : for SQL query context
    """
    input: str="write SQL query to show the number of transactions in the table"

class Output(BaseModel):
    result: str
    
@app.post("/sql_rag_engine")
async def sql_rag_engine_endpoint(query_string: Input):
    try:
        response_data = agent.execute_sql_document_agent(query_string)
        return JSONResponse(content={"output": response_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)