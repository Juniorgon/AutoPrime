from flask import Blueprint, render_template
from sqlalchemy import func
from app.models.models import Marca, Carro, Opcional
main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def dashboard():
    total_carros = Carro.query.count()
    total_marcas = Marca.query.count()
    total_opcionais = Opcional.query.count()
    valor_estoque = db_sum = sum((c.preco for c in Carro.query.all()), 0)
    recentes = Carro.query.order_by(Carro.criado_em.desc()).limit(5).all()
    return render_template("dashboard.html", total_carros=total_carros, total_marcas=total_marcas,
                           total_opcionais=total_opcionais, valor_estoque=valor_estoque, recentes=recentes)
