from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models.models import Opcional
from app.forms import OpcionalForm
opcionais_bp = Blueprint("opcionais", __name__)

@opcionais_bp.get("/")
def listar():
    return render_template("opcionais/lista.html", opcionais=Opcional.query.order_by(Opcional.nome).all())

@opcionais_bp.route("/novo", methods=["GET","POST"])
def novo():
    form=OpcionalForm()
    if form.validate_on_submit():
        db.session.add(Opcional(nome=form.nome.data.strip(), categoria=form.categoria.data, descricao=form.descricao.data))
        db.session.commit(); flash("Opcional cadastrado.", "success"); return redirect(url_for("opcionais.listar"))
    return render_template("opcionais/form.html", form=form, titulo="Novo opcional")

@opcionais_bp.route("/<int:id>/editar", methods=["GET","POST"])
def editar(id):
    item=Opcional.query.get_or_404(id); form=OpcionalForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item); db.session.commit(); flash("Opcional atualizado.", "success"); return redirect(url_for("opcionais.listar"))
    return render_template("opcionais/form.html", form=form, titulo="Editar opcional")

@opcionais_bp.post("/<int:id>/excluir")
def excluir(id):
    item=Opcional.query.get_or_404(id)
    if item.carros: flash("Este opcional está associado a veículos. Remova as associações antes.", "warning")
    else:
        db.session.delete(item); db.session.commit(); flash("Opcional removido.", "success")
    return redirect(url_for("opcionais.listar"))
