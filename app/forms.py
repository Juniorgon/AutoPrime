from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SelectField, TextAreaField, FileField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from app.models.models import Marca, Opcional

class MarcaForm(FlaskForm):
    nome = StringField("Nome da marca", validators=[DataRequired(), Length(max=80)])
    pais_origem = StringField("País de origem", validators=[Optional(), Length(max=60)])
    descricao = StringField("Descrição", validators=[Optional(), Length(max=250)])
    submit = SubmitField("Salvar marca")

class CarroForm(FlaskForm):
    modelo = StringField("Modelo", validators=[DataRequired(), Length(max=100)])
    ano = IntegerField("Ano", validators=[DataRequired(), NumberRange(min=1950, max=2100)])
    cor = StringField("Cor", validators=[DataRequired(), Length(max=40)])
    preco = DecimalField("Preço (R$)", places=2, validators=[DataRequired(), NumberRange(min=0)])
    quilometragem = IntegerField("Quilometragem", validators=[DataRequired(), NumberRange(min=0)])
    combustivel = SelectField("Combustível", choices=[("Flex","Flex"),("Gasolina","Gasolina"),("Etanol","Etanol"),("Diesel","Diesel"),("Híbrido","Híbrido"),("Elétrico","Elétrico")], validators=[DataRequired()])
    cambio = SelectField("Câmbio", choices=[("Manual","Manual"),("Automático","Automático"),("CVT","CVT"),("Automatizado","Automatizado")], validators=[DataRequired()])
    marca_id = SelectField("Marca", coerce=int, validators=[DataRequired()])
    opcionais = SelectMultipleField("Opcionais", coerce=int)
    foto = FileField("Foto do veículo")
    descricao = TextAreaField("Descrição", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Salvar veículo")

    def validate_foto(form, field):
        if field.data and getattr(field.data, "filename", ""):
            ext = field.data.filename.rsplit(".", 1)[-1].lower() if "." in field.data.filename else ""
            if ext not in ("jpg", "png"):
                raise ValidationError("Envie somente imagens JPG ou PNG.")

    def carregar_opcoes(self):
        self.marca_id.choices = [(m.id, m.nome) for m in Marca.query.order_by(Marca.nome).all()]
        self.opcionais.choices = [(o.id, f"{o.nome} · {o.categoria}") for o in Opcional.query.order_by(Opcional.nome).all()]

class OpcionalForm(FlaskForm):
    nome = StringField("Nome do opcional", validators=[DataRequired(), Length(max=80)])
    categoria = SelectField("Categoria", choices=[("Conforto","Conforto"),("Segurança","Segurança"),("Tecnologia","Tecnologia"),("Design","Design"),("Outro","Outro")], validators=[DataRequired()])
    descricao = StringField("Descrição", validators=[Optional(), Length(max=250)])
    submit = SubmitField("Salvar opcional")

class RelatorioForm(FlaskForm):
    marca_id = SelectField("Escolha a marca", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Gerar relatório")
