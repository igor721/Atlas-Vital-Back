from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Mesorregiao(db.Model):
    __tablename__ = "tb_mesorregiao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=True)
    cod_uf: Mapped[int] = mapped_column(ForeignKey("tb_uf.id"), index=True)

    # Relacionamentos
    uf: Mapped["Uf"] = relationship("Uf", back_populates="mesorregioes")
    microrregioes: Mapped[list["Microrregiao"]] = relationship(
        "Microrregiao", back_populates="mesorregiao", cascade="all, delete-orphan"
    )
