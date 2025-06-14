"""Add email verification and password reset tokens to users table."""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bd92a6d7f519'
down_revision = 'ff53e6a9cd48'  # Previous assessment table migration
branch_labels = None
depends_on = None


def upgrade():
    """Add verification and password reset token fields to users table."""
    op.add_column('users', sa.Column('verification_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('verification_token_expires', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('password_reset_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('password_reset_expires', sa.DateTime(timezone=True), nullable=True))
    
    # Create indexes for the token fields for faster lookup
    op.create_index(op.f('ix_users_verification_token'), 'users', ['verification_token'], unique=False)
    op.create_index(op.f('ix_users_password_reset_token'), 'users', ['password_reset_token'], unique=False)


def downgrade():
    """Remove verification and password reset token fields from users table."""
    op.drop_index(op.f('ix_users_password_reset_token'), table_name='users')
    op.drop_index(op.f('ix_users_verification_token'), table_name='users')
    op.drop_column('users', 'password_reset_expires')
    op.drop_column('users', 'password_reset_token')
    op.drop_column('users', 'verification_token_expires')
    op.drop_column('users', 'verification_token')
