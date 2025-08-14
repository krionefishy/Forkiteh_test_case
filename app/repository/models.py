from app.repository.base import Base 
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.sql import func


class WalletModel(Base):
    __tablename__ = "wallet_queries"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    wallet_address: Mapped[str] = mapped_column(String, index=True)
    trx_balance: Mapped[float] = mapped_column(Numeric)
    bandwidth: Mapped[float] = mapped_column(Numeric)
    energy: Mapped[float] = mapped_column(Numeric)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())