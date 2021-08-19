"""Add fs_uniquifier

Revision ID: 879a86b2118c
Revises:
Create Date: 2021-08-19 14:27:13.337332

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '879a86b2118c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('fs_uniquifier', sa.String(length=64), nullable=True))

    # update existing rows with unique fs_uniquifier
    import uuid
    user_table = sa.Table('user', sa.MetaData(), sa.Column('id', sa.Integer, primary_key=True),
                          sa.Column('fs_uniquifier', sa.String))
    conn = op.get_bind()
    for row in conn.execute(sa.select([user_table.c.id])):
        conn.execute(user_table.update().values(fs_uniquifier=uuid.uuid4().hex).where(user_table.c.id == row['id']))

    # Work aroud sqlite limitations. See https://alembic.sqlalchemy.org/en/latest/batch.html
    with op.batch_alter_table("user") as batch_op:
        # finally - set nullable to false
        batch_op.alter_column('fs_uniquifier', nullable=False)


def downgrade():
    with op.batch_alter_table("user") as batch_op:
        batch_op.drop_column('fs_uniquifier')
