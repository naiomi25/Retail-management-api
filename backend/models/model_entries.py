from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import db


class Entry(db.Model):
    __tablename__ = "entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    shift: Mapped[str] = mapped_column(String(10), nullable=False)
    net_sales: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    transactions: Mapped[int] = mapped_column(Integer, nullable=False)
    articles: Mapped[int] = mapped_column(Integer, nullable=False)
    accessories: Mapped[int] = mapped_column(Integer, nullable=False)
    apparel: Mapped[int] = mapped_column(Integer, nullable=False)
    footfall: Mapped[int] = mapped_column(Integer, nullable=False)
    average: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    upt: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    cr: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)

    user = relationship("User", back_populates="entries")

    def calculate_metrics(self):

        if self.articles > 0:
            self.average = round(self.net_sales / self.articles, 2)
        else:
            self.average = 0

        if self.articles > 0:
            self.upt = round(self.articles / self.transactions ,2)
        else:
            self.upt = 0
           

        if self.footfall > 0:
            self.cr = round((self.transactions / self.footfall) * 100, 2)
        else:
            self.cr = 0

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "shift": self.shift,
            "net_sales": float(self.net_sales),
            "transactions": self.transactions,
            "articles": self.articles,
            "accessories": self.accessories,
            "apparel": self.apparel,
            "footfall": self.footfall,
            "average": float(self.average) if self.average else 0.0,
            "upt": float(self.upt) if self.upt else 0.0,
            "cr": float(self.cr) if self.cr else 0.0,
        }
