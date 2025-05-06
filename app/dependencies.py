from sqlmodel import create_engine, Session, SQLModel


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"



# Configuracion de la base de datos
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    """Crea una sesion de base de datos"""
    with Session(engine) as session:
        yield session