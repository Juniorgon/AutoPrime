from datetime import datetime
from app import db

carros_opcionais = db.Table(
    "carros_opcionais",
    db.Column("carro_id", db.Integer, db.ForeignKey("carros.id", ondelete="CASCADE"), primary_key=True),
    db.Column("opcional_id", db.Integer, db.ForeignKey("opcionais.id", ondelete="CASCADE"), primary_key=True),
)

class Marca(db.Model):
    __tablename__ = "marcas"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    pais_origem = db.Column(db.String(60))
    descricao = db.Column(db.String(250))
    carros = db.relationship("Carro", back_populates="marca", lazy=True)

    def __repr__(self):
        return self.nome

class Carro(db.Model):
    __tablename__ = "carros"
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(40), nullable=False)
    preco = db.Column(db.Numeric(12, 2), nullable=False)
    quilometragem = db.Column(db.Integer, nullable=False, default=0)
    combustivel = db.Column(db.String(30), nullable=False)
    cambio = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.Text)
    foto = db.Column(db.LargeBinary)
    foto_mimetype = db.Column(db.String(80))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey("marcas.id", ondelete="RESTRICT"), nullable=False)
    marca = db.relationship("Marca", back_populates="carros")
    opcionais = db.relationship("Opcional", secondary=carros_opcionais, back_populates="carros")

class Opcional(db.Model):
    __tablename__ = "opcionais"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(250))
    carros = db.relationship("Carro", secondary=carros_opcionais, back_populates="opcionais")
