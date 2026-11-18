from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.models import Marca
from app.forms import MarcaForm
marcas_bp = Blueprint("marcas", __name__)

@marcas_bp.route("/")
def listar():
    return render_template("marcas/lista.html", marcas=Marca.query.order_by(Marca.nome).all())

@marcas_bp.route("/nova", methods=["GET","POST"])
def nova():
    form = MarcaForm()
    if form.validate_on_submit():
        marca = Marca(nome=form.nome.data.strip(), pais_origem=form.pais_origem.data, descricao=form.descricao.data)
        db.session.add(marca); db.session.commit()
        flash("Marca cadastrada com sucesso.", "success")
        return redirect(url_for("marcas.listar"))
    return render_template("marcas/form.html", form=form, titulo="Nova marca")

@marcas_bp.route("/<int:id>/editar", methods=["GET","POST"])
def editar(id):
    marca = Marca.query.get_or_404(id); form = MarcaForm(obj=marca)
    if form.validate_on_submit():
        form.populate_obj(marca); db.session.commit()
        flash("Marca atualizada.", "success"); return redirect(url_for("marcas.listar"))
    return render_template("marcas/form.html", form=form, titulo="Editar marca")

@marcas_bp.post("/<int:id>/excluir")
def excluir(id):
    marca = Marca.query.get_or_404(id)
    if marca.carros:
        flash("Não é possível excluir: esta marca possui veículos cadastrados.", "warning")
    else:
        db.session.delete(marca); db.session.commit(); flash("Marca removida.", "success")
    return redirect(url_for("marcas.listar"))
