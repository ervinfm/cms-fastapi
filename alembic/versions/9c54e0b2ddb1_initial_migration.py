"""Initial migration

Revision ID: 9c54e0b2ddb1
Revises: 
Create Date: 2025-02-13 03:12:12.588869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = '9c54e0b2ddb1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Definisikan enum terlebih dahulu
user_role_enum = ENUM('admin', 'user', name='userrole', create_type=True)

def upgrade():
    """Perintah untuk upgrade (membuat tabel)"""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('role', user_role_enum, nullable=False, server_default='user'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

    op.create_table(
        'contents',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('body', sa.Text, nullable=False),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    """Perintah untuk rollback (menghapus tabel)"""
    op.drop_table('content')
    op.drop_table('users')
