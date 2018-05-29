"""empty message

Revision ID: 0197291462b6
Revises: 6d8f18d2a2a4
Create Date: 2018-05-28 22:10:18.762699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0197291462b6'
down_revision = '6d8f18d2a2a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_article_category_create_time'), 'article_category', ['create_time'], unique=False)
    op.create_table('article_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_article_tag_create_time'), 'article_tag', ['create_time'], unique=False)
    op.create_table('files',
    sa.Column('uuid', sa.String(length=100), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('view_num', sa.Integer(), nullable=True),
    sa.Column('content_length', sa.Integer(), nullable=True),
    sa.Column('content_type', sa.String(length=50), nullable=True),
    sa.Column('yun_url', sa.String(length=200), nullable=True),
    sa.Column('_file_hash', sa.String(length=50), nullable=False),
    sa.Column('_locked', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('_file_hash'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('flinks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ip')
    )
    op.create_table('article_article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('describe', sa.Text(), nullable=True),
    sa.Column('read_num', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('image_path', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['article_category.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_article_article_create_time'), 'article_article', ['create_time'], unique=False)
    op.create_table('article_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article_article.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_article_comment_create_time'), 'article_comment', ['create_time'], unique=False)
    op.create_table('article_to_tag',
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article_article.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['article_tag.id'], ),
    sa.PrimaryKeyConstraint('article_id', 'tag_id')
    )
    op.create_table('article_user_like',
    sa.Column('ip_id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article_article.id'], ),
    sa.ForeignKeyConstraint(['ip_id'], ['records.id'], ),
    sa.PrimaryKeyConstraint('ip_id', 'article_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_user_like')
    op.drop_table('article_to_tag')
    op.drop_index(op.f('ix_article_comment_create_time'), table_name='article_comment')
    op.drop_table('article_comment')
    op.drop_index(op.f('ix_article_article_create_time'), table_name='article_article')
    op.drop_table('article_article')
    op.drop_table('records')
    op.drop_table('flinks')
    op.drop_table('files')
    op.drop_index(op.f('ix_article_tag_create_time'), table_name='article_tag')
    op.drop_table('article_tag')
    op.drop_index(op.f('ix_article_category_create_time'), table_name='article_category')
    op.drop_table('article_category')
    # ### end Alembic commands ###