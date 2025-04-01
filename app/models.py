from sqlmodel import SQLModel, Field
# modelos de la aplicacion

class JugadorBase(SQLModel):
    nombre: str = Field(index=True)
    edad: int | None = Field(default=None, index=True)
    nickname: str


class Jugador(JugadorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()

class JugadorCreate(JugadorBase):
    password : str 

class JugadorPublic(JugadorBase):
    id:int

class JugadorUpdate(SQLModel):
    nombre: str | None = None
    edad: int | None = None
    nickname: str | None = None
    password: str | None = None
    
