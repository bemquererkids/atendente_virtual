"""Criar tabela historico_conversa

Revision ID: 554b95f84148
Revises: 
Create Date: 2025-04-28 21:15:40.634610

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '554b95f84148'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('historico_conversa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telefone_usuario', sa.String(length=30), nullable=False),
    sa.Column('mensagem_usuario', sa.Text(), nullable=False),
    sa.Column('resposta_clara', sa.Text(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('clinicas', schema=None) as batch_op:
        batch_op.alter_column('nome',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('cidade',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('contexto', schema=None) as batch_op:
        batch_op.alter_column('telefone_usuario',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('ultima_interacao',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('ultima_resposta',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('dados',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=sa.JSON(),
               existing_nullable=True)
        batch_op.drop_constraint('context_user_phone_key', type_='unique')

    with op.batch_alter_table('perguntas_frequentes', schema=None) as batch_op:
        batch_op.alter_column('pergunta',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('resposta',
               existing_type=sa.TEXT(),
               nullable=True)

    with op.batch_alter_table('profissionais', schema=None) as batch_op:
        batch_op.alter_column('nome',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('especialidade',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profissionais', schema=None) as batch_op:
        batch_op.alter_column('especialidade',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('nome',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    with op.batch_alter_table('perguntas_frequentes', schema=None) as batch_op:
        batch_op.alter_column('resposta',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('pergunta',
               existing_type=sa.TEXT(),
               nullable=False)

    with op.batch_alter_table('contexto', schema=None) as batch_op:
        batch_op.create_unique_constraint('context_user_phone_key', ['telefone_usuario'])
        batch_op.alter_column('dados',
               existing_type=sa.JSON(),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=True)
        batch_op.alter_column('ultima_resposta',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('ultima_interacao',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('telefone_usuario',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('clinicas', schema=None) as batch_op:
        batch_op.alter_column('cidade',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('nome',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    op.drop_table('historico_conversa')
    # ### end Alembic commands ###
