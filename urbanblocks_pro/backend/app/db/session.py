from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urbanblocks_pro.backend.app.db.base import Base
import os
from dotenv import load_dotenv

# Get project root and load .env
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
env_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not set in .env file")

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
