"""create posts table

Revision ID: 6526f7648578
Revises: 
Create Date: 2022-02-21 21:02:24.906374

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision = "6526f7648578"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, primary_key=False, nullable=False),
        sa.Column("content", sa.String, primary_key=False, nullable=False),
        sa.Column(
            "published",
            sa.Boolean,
            primary_key=False,
            nullable=False,
            server_default="TRUE",
        ),
        sa.Column(
            "created_at",
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
