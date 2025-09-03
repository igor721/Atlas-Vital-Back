from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Uf(db.Model):
    __tablename__ = "tb_uf"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sigla: Mapped[str] = mapped_column(Text, nullable=True, index=True)
    nome: Mapped[str] = mapped_column(Text, nullable=True)

    cod_regiao: Mapped[int] = mapped_column(ForeignKey("tb_regiao.id"), index=True)

    # Relacionamentos
    regiao: Mapped["Regiao"] = relationship("Regiao", back_populates="ufs")
    mesorregioes: Mapped[list["Mesorregiao"]] = relationship(
        "Mesorregiao", back_populates="uf", cascade="all, delete-orphan"
    )
    municipios: Mapped[list["Municipio"]] = relationship(
        "Municipio", back_populates="uf", cascade="all, delete-orphan"
    )
    estatisticas: Mapped[list["UfEstatistica"]] = relationship(
        "UfEstatistica", back_populates="uf", cascade="all, delete-orphan"
    )
