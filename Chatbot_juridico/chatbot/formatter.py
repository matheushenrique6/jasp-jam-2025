import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME
from chatbot.prompts import QUEIXA_PROMPT

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

MODELO_OXIDACAO = """
FATO
Declara a demandante que, na data de {data_compra}, comprou um aparelho {produto}, de marca {marca}, pelo valor de R$ {valor_pago}, junto à loja {loja}.
Dado isso, o produto apresentou vício de qualidade. A ordem de serviço de nº {ordem_servico}, registrada em {data_ordem_servico}, não solucionou o problema.

PEDIDO
1 - Citação das demandadas;
2 - Restituição do valor pago de R$ {valor_pago};
3 - Pagamento de indenização por danos morais no valor de R$ {valor_indenizacao};
4 - Inversão do ônus da prova.
"""

def gerar_peticao_oxidacao(dados):
    texto = MODELO_OXIDACAO.format(
        data_compra=dados.data_compra,
        produto=dados.produto,
        marca=dados.marca,
        valor_pago=f"{dados.valor_pago:,.2f}",
        loja=dados.loja,
        ordem_servico=dados.ordem_servico,
        data_ordem_servico=dados.data_ordem_servico,
        valor_indenizacao=f"{dados.valor_indenizacao:,.2f}"
    )
    # Refinar a linguagem com Gemini
    response = model.generate_content([QUEIXA_PROMPT, texto])
    return response.text.strip()
