from pathlib import Path
import os
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import event

# Garantir que a base de dados SQLite fica sempre no diretório 'backend'
BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("ICMAV_DATA_DIR") or str(BACKEND_DIR)).expanduser().resolve()
DATA_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
sqlite_path = DATA_DIR / "app.db"
# Create the database privately before SQLite opens it, preserving existing content.
fd = os.open(sqlite_path, os.O_CREAT | os.O_RDWR, 0o600)
os.close(fd)
sqlite_path.chmod(0o600)
sqlite_url = f"sqlite:///{sqlite_path.as_posix()}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


@event.listens_for(engine, "connect")
def secure_sqlite_connection(connection, _):
    connection.execute("PRAGMA secure_delete=ON")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    from .crud import migrate_secret_settings
    with Session(engine) as session:
        migrate_secret_settings(session)


def get_session():
    with Session(engine) as session:
        yield session
