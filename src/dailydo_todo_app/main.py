from fastapi import FastAPI
from sqlmodel import SQLModel, Field

#creating models here for the database schema

class Todo(SQLModel, table= True ):
    id: int | None  = Field(default=None, primary_key= True)
    content: str = Field(index= True, min_length = 3, max_length = 100)
    is_completed: bool = Field(default= False)


app : FastAPI = FastAPI()

@app.get('/')
async def root_function():
    return {
        "message": "Hey you will get a good job InnShaAllah"
    }

@app.get("/todos/")
async def todos_function():
    return {
        "content": "No todos found"
    }