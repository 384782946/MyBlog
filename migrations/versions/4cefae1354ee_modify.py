"""modify

Revision ID: 4cefae1354ee
Revises: 51f5ccfba190
Create Date: 2016-07-23 13:16:09.932365

"""

# revision identifiers, used by Alembic.
revision = '4cefae1354ee'
down_revision = '51f5ccfba190'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('title', sa.String(length=128), nullable=True))
    op.create_index('ix_posts_title', 'posts', ['title'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_title', 'posts')
    op.drop_column('posts', 'title')
    ### end Alembic commands ###
