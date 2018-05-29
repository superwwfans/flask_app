"""empty message

Revision ID: 6d8f18d2a2a4
Revises: 
Create Date: 2018-05-27 22:25:17.691816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d8f18d2a2a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('strcode', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.Column('login_num', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('avatar_hash', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('permission_handler',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('p_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['p_id'], ['permission_permission.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('p_id')
    )
    op.create_table('permission_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('p_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['p_id'], ['permission_permission.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('p_id')
    )
    op.create_table('permission_to_role',
    sa.Column('p_id', sa.Integer(), nullable=False),
    sa.Column('r_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['p_id'], ['permission_permission.id'], ),
    sa.ForeignKeyConstraint(['r_id'], ['permission_role.id'], ),
    sa.PrimaryKeyConstraint('p_id', 'r_id')
    )
    op.create_table('permission_user_to_role',
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('r_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['r_id'], ['permission_role.id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('u_id', 'r_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('permission_user_to_role')
    op.drop_table('permission_to_role')
    op.drop_table('permission_menu')
    op.drop_table('permission_handler')
    op.drop_table('users')
    op.drop_table('permission_role')
    op.drop_table('permission_permission')
    # ### end Alembic commands ###