from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from dailydo_todo_app import setting


#creating models here for the database schema
class Todo(SQLModel, table= True ):
    id: int | None  = Field(default=None, primary_key= True)
    content: str = Field(index= True, min_length = 3, max_length = 100)
    is_completed: bool = Field(default= False)


# creating one engine for sending the SQL data converted data into database
connection_string : str = str (setting.DATABASE_URL)
engine = create_engine(connection_string, connect_args = {"sslmode" : "require"}, pool_recycle = 300, pool_size = 10, echo=True)

SQLModel.metadata.create_all(engine)

todo1 : Todo = Todo(content = "first task")
todo2: Todo = Todo(content = "second task")

session = Session(engine)

session.add(todo1)
session.add(todo2)
print(f"ToDo1- {todo1} ||  ToDo2- {todo2}")
session.commit()
session.close()

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