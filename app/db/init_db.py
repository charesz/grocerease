from app.db.session import main_engine, reporting_engine, MainBase, ReportingBase
 
# Import all models so SQLAlchemy registers them before create_all
from app.models import user, category, product, order, cart          # noqa
from app.models import reporting                                       # noqa
 
 
def init_db():
    MainBase.metadata.create_all(bind=main_engine)
    ReportingBase.metadata.create_all(bind=reporting_engine)
    print("All tables created.")
 
 