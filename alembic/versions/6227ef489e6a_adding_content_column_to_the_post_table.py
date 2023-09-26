"""adding content column to the post table

Revision ID: 6227ef489e6a
Revises: f981b2be6862
Create Date: 2023-09-25 20:48:22.525596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6227ef489e6a'
down_revision: Union[str, None] = 'f981b2be6862'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
