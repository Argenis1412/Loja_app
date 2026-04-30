from infrastructure.database import SessionLocal
from infrastructure.db.models.recibo_models import ReciboModel


def clear_db():
    db = SessionLocal()
    try:
        db.query(ReciboModel).delete()
        db.commit()
    finally:
        db.close()
