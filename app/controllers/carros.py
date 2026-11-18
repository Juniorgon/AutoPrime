from flask import Blueprint, render_template, redirect, url_for, flash, send_file, abort
from io import BytesIO
from app import db
from app.models.models import Carro
from app.forms import CarroForm
carros_bp = Blueprint("carros", __name__)

@carros_bp.route("/")
def listar():
    termo = __import__("flask").request.args.get("q", "").strip()
    query = Carro.query
    if termo: query = query.filter(Carro.modelo.ilike(f"%{termo}%"))
    return render_template("carros/lista.html", carros=query.order_by(Carro.id.desc()).all(), termo=termo)

@carros_bp.route("/novo", methods=["GET","POST"])
def novo():
    form = CarroForm(); form.carregar_opcoes()
    if form.validate_on_submit():
        upload = form.foto.data
        foto = upload.read() if upload and upload.filename else None
        mimetype = upload.mimetype if foto else None
        from app.models.models import Opcional
        carro = Carro(modelo=form.modelo.data, ano=form.ano.data, cor=form.cor.data,
            preco=form.preco.data, quilometragem=form.quilometragem.data,
            combustivel=form.combustivel.data, cambio=form.cambio.data,
            descricao=form.descricao.data, marca_id=form.marca_id.data,
            opcionais=Opcional.query.filter(Opcional.id.in_(form.opcionais.data)).all() if form.opcionais.data else [],
            foto=foto, foto_mimetype=mimetype)
        db.session.add(carro); db.session.commit()
        flash("Veículo cadastrado.", "success"); return redirect(url_for("carros.listar"))
    return render_template("carros/form.html", form=form, titulo="Novo veículo", carro=None)

@carros_bp.route("/<int:id>/editar", methods=["GET","POST"])
def editar(id):
    carro = Carro.query.get_or_404(id); form = CarroForm(obj=carro); form.carregar_opcoes()
    if not form.is_submitted():
        form.opcionais.data = [o.id for o in carro.opcionais]
    if form.validate_on_submit():
        for campo in ["modelo","ano","cor","preco","quilometragem","combustivel","cambio","descricao","marca_id"]:
            setattr(carro, campo, getattr(form, campo).data)
        from app.models.models import Opcional
        carro.opcionais = Opcional.query.filter(Opcional.id.in_(form.opcionais.data)).all() if form.opcionais.data else []
        upload = __import__("flask").request.files.get("foto")
        if upload and upload.filename:
            carro.foto = upload.read(); carro.foto_mimetype = upload.mimetype
        db.session.commit(); flash("Veículo atualizado.", "success")
        return redirect(url_for("carros.listar"))
    return render_template("carros/form.html", form=form, titulo="Editar veículo", carro=carro)

@carros_bp.post("/<int:id>/excluir")
def excluir(id):
    carro = Carro.query.get_or_404(id); db.session.delete(carro); db.session.commit()
    flash("Veículo removido.", "success"); return redirect(url_for("carros.listar"))

@carros_bp.get("/<int:id>/foto")
def foto(id):
    carro = Carro.query.get_or_404(id)
    if not carro.foto: abort(404)
    return send_file(BytesIO(carro.foto), mimetype=carro.foto_mimetype or "image/jpeg")
