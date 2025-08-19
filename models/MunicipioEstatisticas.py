from sqlalchemy import Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class MunicipioEstatistica(db.Model):
    __tablename__ = "tb_municipio_estatistica"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_municipio: Mapped[int] = mapped_column(ForeignKey("tb_municipio.id"), index=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    total_nascimento: Mapped[int] = mapped_column(Integer, nullable=True)
    total_morte: Mapped[int] = mapped_column(Integer, nullable=True)
    total_casamento: Mapped[int] = mapped_column(Integer, nullable=True)

    municipio: Mapped["Municipio"] = relationship("Municipio", back_populates="estatisticas")

    __table_args__ = (
        Index("idx_municipio_ano", "cod_municipio", "ano", unique=True),
    )
