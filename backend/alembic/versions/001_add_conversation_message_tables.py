"""Add Conversation and Message tables

Revision ID: 001
Revises:
Create Date: 2026-01-26 05:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create Conversation table
    op.create_table(
        'conversation',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index for user_id in Conversation table
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])

    # Create Message table
    op.create_table(
        'message',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for Message table
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('ix_message_user_id', 'message', ['user_id'])
    op.create_index('ix_message_timestamp', 'message', ['timestamp'])


def downgrade() -> None:
    # Drop Message table
    op.drop_index('ix_message_timestamp')
    op.drop_index('ix_message_user_id')
    op.drop_index('ix_message_conversation_id')
    op.drop_table('message')

    # Drop Conversation table
    op.drop_index('ix_conversation_user_id')
    op.drop_table('conversation')