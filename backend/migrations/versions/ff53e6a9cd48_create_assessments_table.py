"""Create assessments table migration."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = 'ff53e6a9cd48'
down_revision = 'abe2fe5fb0b2'  # Reference to the previous migration
branch_labels = None
depends_on = None


def upgrade():
    """Create the assessments table for user assessments."""
    op.create_table(
        'assessments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('data', JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for faster queries
    op.create_index(op.f('ix_assessments_user_id'), 'assessments', ['user_id'], unique=False)
    op.create_index(op.f('ix_assessments_type'), 'assessments', ['type'], unique=False)
    op.create_index(op.f('ix_assessments_created_at'), 'assessments', ['created_at'], unique=False)


def downgrade():
    """Drop the assessments table."""
    op.drop_index(op.f('ix_assessments_created_at'), table_name='assessments')
    op.drop_index(op.f('ix_assessments_type'), table_name='assessments')
    op.drop_index(op.f('ix_assessments_user_id'), table_name='assessments')
    op.drop_table('assessments')
