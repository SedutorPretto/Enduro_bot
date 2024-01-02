from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from datetime import date

from .base import BaseModel


class Staff(BaseModel):
    __tablename__ = 'employees'

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    phone_number: Mapped[int] = mapped_column()
    birth_date: Mapped[date] = mapped_column()
    position: Mapped[str] = mapped_column(nullable=False)
    telegram_photo: Mapped[int] = mapped_column(BigInteger)

    def __str__(self):
        return f'{Staff.first_name} {Staff.surname} {Staff.position}'
