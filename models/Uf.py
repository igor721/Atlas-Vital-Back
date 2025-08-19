from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Uf(db.Model):
    __tablename__ = "tb_uf"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sigla: Mapped[str] = mapped_column(Text, nullable=True)
    nome: Mapped[str] = mapped_column(Text, nullable=True)

    regiao_id: Mapped[int] = mapped_column(ForeignKey("tb_regiao.id"))

    # estatísticas
    total_morte: Mapped[int] = mapped_column(Integer, nullable=True)
    total_nascimento: Mapped[int] = mapped_column(Integer, nullable=True)
    total_casamento: Mapped[int] = mapped_column(Integer, nullable=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=True)

    # relacionamentos
    regiao: Mapped["Regiao"] = relationship("Regiao", back_populates="ufs")
    mesorregioes: Mapped[list["Mesorregiao"]] = relationship(
        "Mesorregiao", back_populates="uf", cascade="all, delete-orphan"
    )
    microrregioes: Mapped[list["Microrregiao"]] = relationship(
        "Microrregiao", back_populates="uf", cascade="all, delete-orphan"
    )
    municipios: Mapped[list["Municipio"]] = relationship(
        "Municipio", back_populates="uf", cascade="all, delete-orphan"
    )
