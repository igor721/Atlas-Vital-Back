from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Municipio(db.Model):
    __tablename__ = "tb_municipio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=True)

    cod_uf: Mapped[int] = mapped_column(ForeignKey("tb_uf.id"), index=True)
    cod_microrregiao: Mapped[int] = mapped_column(ForeignKey("tb_microrregiao.id"), index=True)

    # Relacionamentos
    uf: Mapped["Uf"] = relationship("Uf", back_populates="municipios")
    microrregiao: Mapped["Microrregiao"] = relationship("Microrregiao", back_populates="municipios")
    estatisticas: Mapped[list["MunicipioEstatistica"]] = relationship(
        "MunicipioEstatistica", back_populates="municipio", cascade="all, delete-orphan"
    )
