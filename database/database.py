from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# TODO: move this to env vars later
DATABASE_URL = "sqlite:///./todo.db"
DB_PASSWORD = "admin123"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    print("opening database connection")
    try:
        yield db
    finally:
        print("closing database connection")
        db.close()
