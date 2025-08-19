from sqlalchemy import Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class UfEstatistica(db.Model):
    __tablename__ = "tb_uf_estatistica"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cod_uf: Mapped[int] = mapped_column(ForeignKey("tb_uf.id"), index=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    total_nascimento: Mapped[int] = mapped_column(Integer, nullable=True)
    total_morte: Mapped[int] = mapped_column(Integer, nullable=True)
    total_casamento: Mapped[int] = mapped_column(Integer, nullable=True)

    uf: Mapped["Uf"] = relationship("Uf", back_populates="estatisticas")

    __table_args__ = (
        Index("idx_uf_ano", "cod_uf", "ano", unique=True),
    )
