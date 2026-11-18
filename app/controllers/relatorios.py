from flask import Blueprint, render_template, make_response, redirect, url_for, request
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from app.models.models import Marca, Carro
from app.forms import RelatorioForm

relatorios_bp = Blueprint("relatorios", __name__)

@relatorios_bp.route("/", methods=["GET", "POST"])
def index():
    form = RelatorioForm()
    form.marca_id.choices = [(m.id, m.nome) for m in Marca.query.order_by(Marca.nome).all()]
    if form.validate_on_submit():
        return redirect(url_for("relatorios.index", marca_id=form.marca_id.data))
    marca = None
    carros = []
    marca_id = request.args.get("marca_id", type=int)
    if marca_id:
        marca = Marca.query.get_or_404(marca_id)
        carros = Carro.query.filter_by(marca_id=marca.id).order_by(Carro.modelo).all()
        form.marca_id.data = marca.id
    return render_template("relatorios/index.html", form=form, marca=marca, carros=carros)

@relatorios_bp.get("/marca/<int:marca_id>/pdf")
def pdf(marca_id):
    marca = Marca.query.get_or_404(marca_id)
    carros = Carro.query.filter_by(marca_id=marca.id).order_by(Carro.modelo).all()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                            topMargin=18*mm, bottomMargin=22*mm)
    styles = getSampleStyleSheet()
    story = [Paragraph("Relatório de veículos por marca", styles["Title"]), Spacer(1, 8),
             Paragraph(f"<b>Marca:</b> {marca.nome}", styles["Heading2"]), Spacer(1, 12)]
    data = [["Modelo", "Ano", "Preço (R$)", "KM", "Combustível"]]
    for carro in carros:
        data.append([carro.modelo, str(carro.ano), f"{carro.preco:,.2f}",
                     f"{carro.quilometragem:,}".replace(",", "."), carro.combustivel])
    if len(data) == 1:
        data.append(["Nenhum veículo cadastrado", "", "", "", ""])
    table = Table(data, repeatRows=1, colWidths=[48*mm, 18*mm, 32*mm, 25*mm, 35*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#182536")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), .35, colors.HexColor("#d7dee7")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f3f6fa")]),
        ("FONTSIZE", (0,0), (-1,-1), 8), ("PADDING", (0,0), (-1,-1), 7)
    ]))
    story += [table, Spacer(1, 18),
              Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} · Total de veículos: {len(carros)}", styles["Normal"])]
    doc.build(story)
    response = make_response(buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f'attachment; filename="veiculos-{marca.id}.pdf"'
    return response
