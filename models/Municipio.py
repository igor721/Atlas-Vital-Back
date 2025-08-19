from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.database import db

class Municipio(db.Model):
    __tablename__ = "tb_municipio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=True)

    uf_id: Mapped[int] = mapped_column(ForeignKey("tb_uf.id"))
    microrregiao_id: Mapped[int] = mapped_column(ForeignKey("tb_microrregiao.id"))

    # estatísticas
    total_morte: Mapped[int] = mapped_column(Integer, nullable=True)
    total_nascimento: Mapped[int] = mapped_column(Integer, nullable=True)
    total_casamento: Mapped[int] = mapped_column(Integer, nullable=True)
    ano: Mapped[int] = mapped_column(Integer, nullable=True)

    # relacionamentos
    uf: Mapped["Uf"] = relationship("Uf", back_populates="municipios")
    microrregiao: Mapped["Microrregiao"] = relationship("Microrregiao", back_populates="municipios")
