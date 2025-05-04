from .faq_tool import buscar_faq
from .profissionais_tool import consultar_profissionais
from .gpt_tool import responder_gpt_tool
from .especialidade_tool import responder_especialidade_tool  # ✅ nova importação

tools = [
    buscar_faq,
    consultar_profissionais,
    responder_gpt_tool,
    responder_especialidade_tool  # ✅ nova tool registrada
]