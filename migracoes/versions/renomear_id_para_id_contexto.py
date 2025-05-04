"""Renomeia id para id_contexto na tabela contexto"""

from alembic import op

# ID único da versão (substitua se quiser)
revision = 'renomear_id_para_id_contexto'
down_revision = 'f39d1180893a'  # ← ajuste para o hash correto da última migração
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('contexto', 'id', new_column_name='id_contexto')

def downgrade():
    op.alter_column('contexto', 'id_contexto', new_column_name='id')