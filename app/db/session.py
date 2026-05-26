from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
 
from app.core.config import settings
 
# Main database
main_engine = create_engine(settings.MAIN_DATABASE_URL)
MainSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=main_engine)
 
# Reporting database
reporting_engine = create_engine(settings.REPORTING_DATABASE_URL)
ReportingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=reporting_engine)
 
# Bases
MainBase = declarative_base()
ReportingBase = declarative_base()
 
 
def get_main_db():
    db = MainSessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
def get_reporting_db():
    db = ReportingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        