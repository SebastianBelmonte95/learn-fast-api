"""create votes table

Revision ID: f18abfe91ac4
Revises: d66322e31ec6
Create Date: 2022-02-21 23:24:57.954141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f18abfe91ac4"
down_revision = "d66322e31ec6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "votes",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "post_id",
            sa.Integer,
            sa.ForeignKey("posts.id", ondelete="CASCADE", onupdate="CASCADE"),
            primary_key=True,
            nullable=False,
        ),
    )
    pass


def downgrade():
    op.drop_table("votes")
    pass
