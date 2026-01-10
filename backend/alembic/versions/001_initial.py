"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('discord_id', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('avatar', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Chronicles table
    op.create_table(
        'chronicles',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('game_version', sa.String(10), nullable=False, server_default='v5'),
        sa.Column('storyteller_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_chronicles_storyteller_id', 'chronicles', ['storyteller_id'])

    # Chronicle members table
    op.create_table(
        'chronicle_members',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('chronicle_id', sa.String(36), sa.ForeignKey('chronicles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='player'),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('chronicle_id', 'user_id', name='uq_chronicle_member'),
    )
    op.create_index('ix_chronicle_members_chronicle_id', 'chronicle_members', ['chronicle_id'])
    op.create_index('ix_chronicle_members_user_id', 'chronicle_members', ['user_id'])

    # Characters table
    op.create_table(
        'characters',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('owner_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('chronicle_id', sa.String(36), sa.ForeignKey('chronicles.id', ondelete='SET NULL'), nullable=True),
        sa.Column('game_version', sa.String(10), nullable=False, server_default='v5'),
        sa.Column('sheet', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_characters_owner_id', 'characters', ['owner_id'])
    op.create_index('ix_characters_chronicle_id', 'characters', ['chronicle_id'])

    # Scenes table
    op.create_table(
        'scenes',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('location', sa.String(200), nullable=True),
        sa.Column('chronicle_id', sa.String(36), sa.ForeignKey('chronicles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_active', sa.Boolean, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_scenes_chronicle_id', 'scenes', ['chronicle_id'])

    # Dice rolls table
    op.create_table(
        'dice_rolls',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('character_id', sa.String(36), sa.ForeignKey('characters.id', ondelete='SET NULL'), nullable=True),
        sa.Column('chronicle_id', sa.String(36), sa.ForeignKey('chronicles.id', ondelete='SET NULL'), nullable=True),
        sa.Column('roller_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('game_version', sa.String(10), nullable=False),
        sa.Column('roll_type', sa.String(50), nullable=False),
        sa.Column('dice_pool', sa.Integer, nullable=False),
        sa.Column('difficulty', sa.Integer, nullable=True),
        sa.Column('hunger', sa.Integer, nullable=True),
        sa.Column('result', postgresql.JSONB, nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_dice_rolls_chronicle_id', 'dice_rolls', ['chronicle_id'])
    op.create_index('ix_dice_rolls_character_id', 'dice_rolls', ['character_id'])
    op.create_index('ix_dice_rolls_roller_id', 'dice_rolls', ['roller_id'])


def downgrade() -> None:
    op.drop_table('dice_rolls')
    op.drop_table('scenes')
    op.drop_table('characters')
    op.drop_table('chronicle_members')
    op.drop_table('chronicles')
    op.drop_table('users')
