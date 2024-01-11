from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class BaseModel(DeclarativeBase):
    pass


class Staff(BaseModel):
    __tablename__ = 'employers'

    user_id: Mapped[int] = mapped_column(unique=True, primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    surname: Mapped[str]
    phone_number: Mapped[str]
    birth_date: Mapped[date]
    position: Mapped[str] = mapped_column(nullable=False)
    telegram_photo: Mapped[str]

    def __repr__(self):
        return f'{self.user_id} - {self.first_name} {self.surname} - {self.position}'
