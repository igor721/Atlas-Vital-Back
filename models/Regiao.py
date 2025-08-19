from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Regiao(db.Model):
    __tablename__ = "tb_regiao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sigla: Mapped[str] = mapped_column(Text, nullable=True, index=True)
    nome: Mapped[str] = mapped_column(Text, nullable=True)

    # Relacionamento
    ufs: Mapped[list["Uf"]] = relationship(
        "Uf", back_populates="regiao", cascade="all, delete-orphan"
    )
