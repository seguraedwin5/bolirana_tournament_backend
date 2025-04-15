from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import  Session, select
from contextlib import asynccontextmanager
from .models import Jugador, JugadorCreate, JugadorPublic, JugadorUpdate
from .dependencies import get_session, create_db_and_tables, engine




@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event for the FastAPI application."""
    create_db_and_tables()
    yield
    # Cleanup code can be added here if needed

def hash_password(password: str) -> str:
    """Hash a password template"""
    # Implement your password hashing logic here
    return f"mi password hasheada: 123{password}123"

#inicio de la aplicacion
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/jugadores/", response_model=JugadorPublic)
def create_jugador(*,session:Session = Depends(get_session) ,jugador: JugadorCreate):
    hashed_password = hash_password(jugador.password) # hasheamos la contraseña
    extra_data = {"hashed_password": hashed_password} # creamos un diccionario con los datos extra
    db_jugador = Jugador.model_validate(jugador, update=extra_data) # creamos un objeto Jugador con los datos del cliente y los datos extra
    session.add(db_jugador)
    session.commit()
    session.refresh(db_jugador)
    return db_jugador


@app.get("/jugadores/", response_model=list[JugadorPublic])
def read_jugadores( 
    *,
    session:Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
    ):
    """Obtiene una lista de jugadores paginada"""
    jugadores = session.exec(select(Jugador).offset(offset).limit(limit)).all()
    return jugadores


@app.get("/jugadores/{jugador_id}", response_model=JugadorPublic)
def read_jugador(
    *,
    session:Session = Depends(get_session),
    jugador_id: int
    ):
    with Session(engine) as session:
        jugador = session.get(Jugador, jugador_id)
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return jugador


@app.patch("/jugadores/{jugador_id}", response_model=JugadorPublic, description="Actualiza un jugador existente")
def update_jugador(
    *,
    session:Session = Depends(get_session),
    jugador_id: int,
    jugador: JugadorUpdate
    ):
    db_jugador = session.get(Jugador, jugador_id)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    jugador_data = jugador.model_dump(exclude_unset=True) # se crea un diccionario con los datos a actualizar enviado por el cliente
    extra_data = {}
    if "password" in jugador_data: # si la contraseña es parte de los datos a actualizar, se hashea
        password = jugador_data["password"]
        hashed_password = hash_password(password)
        extra_data["hashed_password"] = hashed_password
    db_jugador.sqlmodel_update(jugador_data, update=extra_data) # actualiza el objeto de la base de datos con los datos del cliente
    session.add(db_jugador) # se añade el objeto a la sesion para que sea actualizado
    session.commit() ## se hace el commit para guardar los cambios en la base de datos
    session.refresh(db_jugador) # se refresca el objeto para que tenga los datos actualizados de la base de datos
    return db_jugador


@app.delete("/jugadores/{jugador_id}", response_model=JugadorPublic, description="Elimina un jugador existente")
def delete_jugador(
    *,
    session:Session = Depends(get_session),
    jugador_id: int
    ):
    db_jugador = session.get(Jugador, jugador_id)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    session.delete(db_jugador)
    session.commit()
    return { "ok": True, "message": "Jugador eliminado"}





