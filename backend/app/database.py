from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine

# Garantir que a base de dados SQLite fica sempre no diretório 'backend'
BACKEND_DIR = Path(__file__).resolve().parent.parent
sqlite_path = BACKEND_DIR / "app.db"
sqlite_url = f"sqlite:///{sqlite_path.as_posix()}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session