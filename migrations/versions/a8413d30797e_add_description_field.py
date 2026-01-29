"""add description field

Revision ID: a8413d30797e
Revises: d111ea0b7563
Create Date: 2026-01-29 17:30:13.619825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8413d30797e'
down_revision = 'd111ea0b7563'
branch_labels = None
depends_on = None


def upgrade():
    """
    Apply changes to the database.
    Only add the missing column since tables already exist on production.
    """
    # Using batch_alter_table for better compatibility (e.g., SQLite)
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))


def downgrade():
    """
    Revert changes from the database.
    Remove only the description column to preserve other data.
    """
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('description')