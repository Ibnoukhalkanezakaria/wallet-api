import uuid
from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    balance = Column(Numeric(12, 2), default=0.00, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
