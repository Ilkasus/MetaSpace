from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://metaspace_db_user:eN9p7YNSVDXKFlT3n7ElmPDFprKA8Wj4@dpg-d0rctummcj7s7385trg0-a.oregon-postgres.render.com/metaspace_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
