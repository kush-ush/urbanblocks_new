import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load .env from project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
env_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in .env")

# Engine with pool_pre_ping ensures DB connection is valid before queries
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    """
    Dependency to get a SQLAlchemy session.
    Use as: db: Session = Depends(get_db) in FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
