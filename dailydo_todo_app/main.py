from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from dailydo_todo_app import setting
from typing import Annotated
from contextlib import asynccontextmanager

#creating models here for the database schema
class Todo(SQLModel, table= True ):
    id: int | None  = Field(default=None, primary_key= True)
    content: str = Field(index= True, min_length = 3, max_length = 100)
    is_completed: bool = Field(default= False)


# creating one engine for sending the SQL data converted data into database
connection_string: str = str(setting.DATABASE_URL).strip().strip('"').strip("'")
if connection_string.startswith("postgresql://"):
    connection_string = connection_string.replace("postgresql://", "postgresql+psycopg://", 1)

    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300, pool_size=10, echo=True)
    # engine = create_engine(connection_string, pool_recycle=300, pool_size=10, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

# todo1 : Todo = Todo(content = "first task")
# todo2: Todo = Todo(content = "second task")

# session = Session(engine)

# session.add(todo1)
# session.add(todo2)
# print(f"ToDo1- {todo1} ||  ToDo2- {todo2}")
# session.commit()
# session.close()

def session_function():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Creating Tables')
    create_tables()
    print("Tables Created")
    yield 

app : FastAPI = FastAPI(lifespan = lifespan, title= "DailyDo")

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

@app.get("/todos/")
async def get_all_todos(session: Annotated[Session, Depends(session_function)]):
    statement= select(Todo)
    todos = session.exec(statement).all()
    return todos

@app.get("/todos/{id}", response_model= Todo)
async def get_single_todo(id: int, session:Annotated[Session, Depends(session_function)]):
    todo = session.exec(select(Todo).where(Todo.id == id)).first()
    return todo

@app.post("/todos/", response_model = Todo)
async def create_todos(todo: Todo, session:Annotated[Session, Depends(session_function)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.put("/todos/{id}")
async def update_function(id:int, todo:Todo, session:Annotated[Session, Depends(session_function)]):
    existing_todo = session.exec(select(Todo).where(Todo.id == id)).first()
    if existing_todo:
        existing_todo.content = todo.content
        existing_todo.is_completed = todo.is_completed
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException (status_code= 404, detail= "No task found")


@app.delete("/todos/{id}")
async def delete_function(id: int, session: Annotated[Session, Depends(session_function)]):
    todo= session.exec(select(Todo).where(Todo.id == id)).first()
    if todo: 
        session.delete(todo)
        session.commit()
        session.refresh(todo)
        return {"message" : "Task successfully deleted"}
    else: 
        raise HTTPException(status_code = 404, detail= "No task found")
