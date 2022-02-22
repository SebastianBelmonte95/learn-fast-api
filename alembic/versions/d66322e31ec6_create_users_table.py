"""create users table

Revision ID: d66322e31ec6
Revises: 6526f7648578
Create Date: 2022-02-21 21:17:32.231523

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision = "d66322e31ec6"
down_revision = "6526f7648578"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, primary_key=False, nullable=False),
        sa.Column(
            "created_at",
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
