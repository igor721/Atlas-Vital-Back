from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from helpers.database import db

class Cartorio(db.Model):
    __tablename__ = "tb_cartorio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    email: Mapped[str] = mapped_column(Text, nullable=True, index=True)
    cnpj: Mapped[str] = mapped_column(Text, nullable=True, unique=True, index=True)
