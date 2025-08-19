from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db


class Regiao(db.Model):
    __tablename__ = "tb_regiao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sigla: Mapped[str] = mapped_column(Text, nullable=True)
    nome: Mapped[str] = mapped_column(Text, nullable=True)

    # estatísticas
    total_morte: Mapped[int] = mapped_column(Integer, nullable=True)
    total_nascimento: Mapped[int] = mapped_column(Integer, nullable=True)
    total_casamento: Mapped[int] = mapped_column(Integer, nullable=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=True)

    # relacionamentos
    ufs: Mapped[list["Uf"]] = relationship(
        "Uf", back_populates="regiao", cascade="all, delete-orphan"
    )