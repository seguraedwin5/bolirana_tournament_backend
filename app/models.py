from sqlmodel import SQLModel, Field, Relationship
# modelos de la aplicacion

# modelos de Equipos

class EquipoBase(SQLModel):
    nombre: str = Field(index=True)
    ciudad: str = Field(index=True)

class Equipo(EquipoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jugadores: list["Jugador"] = Relationship(back_populates="equipo")

class EquipoCreate(EquipoBase):
    pass

class EquipoPublic(EquipoBase):
    id: int

class EquipoUpdate(SQLModel):
    nombre: str | None = None
    ciudad: str | None = None
     

class JugadorBase(SQLModel):
    nombre: str = Field(index=True)
    edad: int | None = Field(default=None, index=True)
    nickname: str

    equipo_id: int | None = Field(default=None, foreign_key="equipo.id")

class Jugador(JugadorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    equipo: Equipo | None = Relationship(back_populates="jugadores")
    
class JugadorCreate(JugadorBase):
    password : str 

class JugadorPublic(JugadorBase):
    id:int

class JugadorUpdate(SQLModel):
    nombre: str | None = None
    edad: int | None = None
    nickname: str | None = None
    password: str | None = None
    equipo_id: int | None = None
