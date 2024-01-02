from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from datetime import date

from .base import BaseModel


class Staff(BaseModel):
    __tablename__ = 'employees'

    telegram_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True, nullable=False)
    first_name: Mapped[str] = mapped_column()
    second_name: Mapped[str] = mapped_column()
    phone_number: Mapped[int] = mapped_column()
    birth_date: Mapped[date] = mapped_column()
    position: Mapped[str] = mapped_column(nullable=False)

    def __str__(self):
        return f'{Staff.first_name} {Staff.second_name} {Staff.position}'
