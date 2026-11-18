"""Criação inicial das entidades da concessionária."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("marcas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(80), nullable=False, unique=True),
        sa.Column("pais_origem", sa.String(60)),
        sa.Column("descricao", sa.String(250)))
    op.create_table("carros",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("modelo", sa.String(100), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("cor", sa.String(40), nullable=False),
        sa.Column("preco", sa.Numeric(12, 2), nullable=False),
        sa.Column("quilometragem", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("combustivel", sa.String(30), nullable=False),
        sa.Column("cambio", sa.String(30), nullable=False),
        sa.Column("descricao", sa.Text()),
        sa.Column("foto", sa.LargeBinary()),
        sa.Column("foto_mimetype", sa.String(80)),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.Column("marca_id", sa.Integer(), sa.ForeignKey("marcas.id", ondelete="RESTRICT"), nullable=False))
    op.create_table("opcionais",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(80), nullable=False, unique=True),
        sa.Column("categoria", sa.String(50), nullable=False),
        sa.Column("descricao", sa.String(250)))
    op.create_table("carros_opcionais",
        sa.Column("carro_id", sa.Integer(), sa.ForeignKey("carros.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("opcional_id", sa.Integer(), sa.ForeignKey("opcionais.id", ondelete="CASCADE"), primary_key=True))

def downgrade():
    op.drop_table("carros_opcionais")
    op.drop_table("opcionais")
    op.drop_table("carros")
    op.drop_table("marcas")
