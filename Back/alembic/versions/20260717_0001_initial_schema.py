"""Cria o esquema inicial do Voxify."""

from alembic import op
import sqlalchemy as sa

revision = "20260717_0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False, unique=True),
        sa.Column("senha", sa.String(length=255), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_usuarios_id", "usuarios", ["id"])
    op.create_table(
        "arquivos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("nome_do_audio", sa.String(length=255), nullable=False),
        sa.Column("url_audio", sa.Text(), nullable=False),
        sa.Column("tipo_arquivo", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="enviado"),
        sa.Column("data_upload", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_arquivos_id", "arquivos", ["id"])
    op.create_table(
        "transcricoes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("arquivo_id", sa.Integer(), sa.ForeignKey("arquivos.id", ondelete="CASCADE"), nullable=False),
        sa.Column("texto", sa.Text(), nullable=False),
        sa.Column("idioma", sa.String(length=10), nullable=True, server_default="pt"),
        sa.Column("data_criacao", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_transcricoes_id", "transcricoes", ["id"])

def downgrade() -> None:
    op.drop_index("ix_transcricoes_id", table_name="transcricoes")
    op.drop_table("transcricoes")
    op.drop_index("ix_arquivos_id", table_name="arquivos")
    op.drop_table("arquivos")
    op.drop_index("ix_usuarios_id", table_name="usuarios")
    op.drop_table("usuarios")
