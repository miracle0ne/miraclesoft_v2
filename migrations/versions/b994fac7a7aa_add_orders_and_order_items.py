"""add orders and order items

Revision ID: b994fac7a7aa
Revises: f187b554aa64
Create Date: 2026-08-08 17:44:54.747349
"""

from alembic import op
import sqlalchemy as sa


revision = 'b994fac7a7aa'
down_revision = 'f187b554aa64'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('order_id', sa.Integer(), nullable=True)
        )

        batch_op.alter_column(
            'price',
            existing_type=sa.Integer(),
            type_=sa.Float(),
            existing_nullable=False
        )

        batch_op.drop_constraint(
            'order_item_oder_id_fkey',
            type_='foreignkey'
        )

        batch_op.create_foreign_key(
            'order_item_order_id_fkey',
            'orders',
            ['order_id'],
            ['id']
        )

        batch_op.drop_column('oder_id')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('created_at', sa.DateTime(), nullable=True)
        )

        batch_op.alter_column(
            'user_id',
            existing_type=sa.Integer(),
            nullable=False
        )

        batch_op.drop_column('create_at')


def downgrade():
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('create_at', sa.DateTime(), nullable=True)
        )

        batch_op.alter_column(
            'user_id',
            existing_type=sa.Integer(),
            nullable=True
        )

        batch_op.drop_column('created_at')

    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('oder_id', sa.Integer(), nullable=True)
        )

        batch_op.drop_constraint(
            'order_item_order_id_fkey',
            type_='foreignkey'
        )

        batch_op.create_foreign_key(
            'order_item_oder_id_fkey',
            'orders',
            ['oder_id'],
            ['id']
        )

        batch_op.alter_column(
            'price',
            existing_type=sa.Float(),
            type_=sa.Integer(),
            existing_nullable=False
        )

        batch_op.drop_column('order_id')
