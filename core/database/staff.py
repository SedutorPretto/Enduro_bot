from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from datetime import date

from core.database.base import BaseModel


class Staff(BaseModel):
    __tablename__ = 'employees'

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    surname: Mapped[str]
    phone_number: Mapped[int]
    birth_date: Mapped[date]
    position: Mapped[str] = mapped_column(nullable=False)
    telegram_photo: Mapped[int] = mapped_column(BigInteger)

    def __str__(self):
        return f'{Staff.first_name} {Staff.surname} {Staff.position}'
