from dailydo_todo_app import setting
from sqlmodel import SQLModel, create_engine, Session
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dailydo_todo_app.main import app, session_function


# creating one engine for sending the SQL data converted data into database
connection_string: str = str(setting.Test_DATABASE_URL).strip().strip('"').strip("'")
if connection_string.startswith("postgresql://"):
    connection_string = connection_string.replace("postgresql://", "postgresql+psycopg://", 1)

    engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300, pool_size=10, echo=True)
    # engine = create_engine(connection_string, pool_recycle=300, pool_size=10, echo=True)



def test_root():
    client = TestClient(app = app )
    response = client.get("/")
    data= response.json()
    assert response.status_code == 200
    assert data == {"message" : "Welcome to DailyDo todo app"}


def test_create_todo():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        def db_session_override():
            return session
    app.dependency_overrides[session_function] = db_session_override
    client = TestClient(app = app)
    test_todo = {"context": "create_todo_test", "is_completed": False}
    response = client.post('/todos/', json=test_todo )
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == test_todo["content"]


def test_get_all():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        def db_session_override():
            return session
    app.dependency_overrides[session_function] = db_session_override
    client = TestClient(app = app)
    response = client.get('/todos/')
    assert response.status_code == 200
