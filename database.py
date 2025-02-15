from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL uchun ulanish URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:azizbek006@localhost/lmsdatabase"
# Engine yaratish
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal yaratish
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base obyektini yaratish
Base = declarative_base()