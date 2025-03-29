from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

class Jugador(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    edad: int
    nickname: str

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event for the FastAPI application."""
    create_db_and_tables()
    yield
    # Cleanup code can be added here if needed


#inicio de la aplicacion
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/jugadores/", response_model=Jugador)
def create_jugador(jugador: Jugador):
    with Session(engine) as session:
        session.add(jugador)
        session.commit()
        session.refresh(jugador)
    return jugador

@app.get("/jugadores/", response_model=list[Jugador])
def read_jugadores():
    with Session(engine) as session:
        jugadores = session.exec(select(Jugador)).all()
    return jugadores
