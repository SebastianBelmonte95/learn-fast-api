"""add user_id column to posts table

Revision ID: 085027ad7caf
Revises: f18abfe91ac4
Create Date: 2022-02-21 23:40:03.295938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "085027ad7caf"
down_revision = "f18abfe91ac4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("posts", "user_id")
