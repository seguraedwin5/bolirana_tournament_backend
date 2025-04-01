from fastapi import FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# modelos de la aplicacion
class JugadorBase(SQLModel):
    nombre: str = Field(index=True)
    edad: int | None = Field(default=None, index=True)
    nickname: str


class Jugador(JugadorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    

class JugadorCreate(JugadorBase):
    pass

class JugadorPublic(JugadorBase):
    id:int

class JugadorUpdate(SQLModel):
    #pendiente de implementacion
    pass 


# Configuracion de la base de datos
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

@app.post("/jugadores/", response_model=JugadorPublic)
def create_jugador(jugador: JugadorCreate):
    with Session(engine) as session:
        db_jugador = Jugador.model_validate(jugador)
        session.add(db_jugador)
        session.commit()
        session.refresh(db_jugador)
    return db_jugador

@app.get("/jugadores/", response_model=list[JugadorPublic])
def read_jugadores(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        jugadores = session.exec(select(Jugador).offset(offset).limit(limit)).all()
    return jugadores

@app.get("/jugadores/{jugador_id}", response_model=JugadorPublic)
def read_jugador(jugador_id: int):
    with Session(engine) as session:
        jugador = session.get(Jugador, jugador_id)
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return jugador
