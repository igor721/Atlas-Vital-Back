from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Microrregiao(db.Model):
    __tablename__ = "tb_microrregiao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=True)

    mesorregiao_id: Mapped[int] = mapped_column(ForeignKey("tb_mesorregiao.id"))
    uf_id: Mapped[int] = mapped_column(ForeignKey("tb_uf.id"))

    # relacionamentos
    mesorregiao: Mapped["Mesorregiao"] = relationship("Mesorregiao", back_populates="microrregioes")
    uf: Mapped["Uf"] = relationship("Uf", back_populates="microrregioes")
    municipios: Mapped[list["Municipio"]] = relationship(
        "Municipio", back_populates="microrregiao", cascade="all, delete-orphan"
    )
