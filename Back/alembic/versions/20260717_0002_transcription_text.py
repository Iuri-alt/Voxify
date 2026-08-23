"""Adiciona texto e idioma às transcrições existentes."""

from alembic import op
import sqlalchemy as sa

revision = "20260717_0002"
down_revision = "20260717_0001"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column("transcricoes", sa.Column("texto", sa.Text(), nullable=True))
    op.add_column("transcricoes", sa.Column("idioma", sa.String(length=10), nullable=True, server_default="pt"))
    op.execute("UPDATE transcricoes SET texto = 'Transcrição legada indisponível.' WHERE texto IS NULL")
    op.alter_column("transcricoes", "texto", nullable=False)
    op.alter_column(
        "transcricoes",
        "data_criacao",
        existing_type=sa.TIMESTAMP(timezone=False),
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="data_criacao AT TIME ZONE 'UTC'",
    )

def downgrade() -> None:
    op.alter_column(
        "transcricoes",
        "data_criacao",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=sa.TIMESTAMP(timezone=False),
        postgresql_using="data_criacao AT TIME ZONE 'UTC'",
    )
    op.drop_column("transcricoes", "idioma")
    op.drop_column("transcricoes", "texto")
