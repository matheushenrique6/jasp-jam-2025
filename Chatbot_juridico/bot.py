import logging
import os
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    ApplicationBuilder,
)
from chatbot.collector import QueixaOxidacaoData
from chatbot.formatter import gerar_peticao_oxidacao
from chatbot.pdf_generator import gerar_pdf_com_cadastro as gerar_pdf
import httpx
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LARAVEL_API = os.getenv("LARAVEL_API_URL", "http://127.0.0.1:8000/api/messages")

logging.basicConfig(level=logging.INFO)

# Estados da conversa
(
    NOME_DEMANDANTE,
    CPF_CNPJ,
    NOME_SOCIAL,
    EMAIL,
    CONFIRMAR_EMAIL,
    TELEFONE,
    WHATSAPP,
    CEP,
    LOGRADOURO,
    NUMERO,
    COMPLEMENTO,
    BAIRRO,
    CIDADE,
    UF,
    CONFIRMAR_CADASTRO,
    NOME,
    DATA_COMPRA,
    PRODUTO,
    MARCA,
    VALOR,
    LOJA,
    ORDEM,
    DATA_ORDEM,
    VALOR_INDEMNIZACAO,
) = range(24)

user_data_dict = {}

# --------------------------
# Função para enviar mensagens para Laravel
# --------------------------
async def log_message(chat_id, text, direction="incoming"):
    payload = {
        "chat_id": str(chat_id),
        "text": text,
        "direction": direction
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post(LARAVEL_API, json=payload)
        except Exception as e:
            print(f"Erro ao enviar para Laravel: {e}")

# --------------------------
# Função auxiliar para enviar mensagens do bot e logar
# --------------------------
async def reply_and_log(update: Update, text: str):
    user_id = update.message.from_user.id
    await update.message.reply_text(text)
    await log_message(user_id, text, direction="outgoing")

# --------------------------
# Handlers
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_and_log(update, "Olá! Vamos começar cadastrando seus dados.\nQual seu nome completo?")
    return NOME_DEMANDANTE

async def nome_demandante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id] = QueixaOxidacaoData()
    user_data_dict[user_id].nome_demandante = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "CPF/CNPJ *") or CPF_CNPJ

async def cpf_cnpj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].cpf_cnpj = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Nome Social (opcional)") or NOME_SOCIAL

async def nome_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].nome_social = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "E-mail *") or EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].email = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Confirme seu e-mail *") or CONFIRMAR_EMAIL

async def confirmar_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].confirmar_email = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Telefone *") or TELEFONE

async def telefone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].telefone = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Este telefone possui Whatsapp? (sim/não)") or WHATSAPP

async def whatsapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].whatsapp = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "CEP") or CEP

async def cep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].cep = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Logradouro *") or LOGRADOURO

async def logradouro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].logradouro = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Número *") or NUMERO

async def numero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].numero = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Complemento (opcional)") or COMPLEMENTO

async def complemento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].complemento = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Bairro *") or BAIRRO

async def bairro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].bairro = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Cidade *") or CIDADE

async def cidade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].cidade = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "UF *") or UF

async def uf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].uf = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Declaro que resido no endereço informado. \nDigite 'ok' para confirmar e continuar com a queixa.") or CONFIRMAR_CADASTRO

async def confirmar_cadastro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Cadastro concluído! Agora vamos à queixa do produto.\nQual o seu nome?") or NOME

# --------------------------
# Fluxo da queixa
# --------------------------
async def nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].nome_autor = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Data da compra? (dd/mm/aaaa)") or DATA_COMPRA

async def data_compra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].data_compra = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Qual o produto comprado?") or PRODUTO

async def produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].produto = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Qual a marca do produto?") or MARCA

async def marca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].marca = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Qual o valor pago?") or VALOR

async def valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].valor_pago = float(update.message.text.replace(",", "."))
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Qual a loja onde comprou?") or LOJA

async def loja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].loja = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Número da ordem de serviço?") or ORDEM

async def ordem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].ordem_servico = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Data da ordem de serviço? (dd/mm/aaaa)") or DATA_ORDEM

async def data_ordem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].data_ordem_servico = update.message.text
    await log_message(user_id, update.message.text, "incoming")
    return await reply_and_log(update, "Valor da indenização desejada?") or VALOR_INDEMNIZACAO

async def valor_indenizacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].valor_indenizacao = float(update.message.text.replace(",", "."))
    await log_message(user_id, update.message.text, "incoming")

    peticao = gerar_peticao_oxidacao(user_data_dict[user_id])
    arquivo_pdf = gerar_pdf(
        user_data_dict[user_id].dict(),
        peticao,
        nome_arquivo=f"peticao_{user_id}.pdf",
        titulo="Petição de Queixa"
    )

    with open(arquivo_pdf, "rb") as f:
        await update.message.reply_document(document=f, filename=arquivo_pdf, caption="Sua petição está pronta!")
    return ConversationHandler.END

# --------------------------
# Cancelamento
# --------------------------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply_and_log(update, "Operação cancelada.")
    return ConversationHandler.END

# --------------------------
# Main
# --------------------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NOME_DEMANDANTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, nome_demandante)],
            CPF_CNPJ: [MessageHandler(filters.TEXT & ~filters.COMMAND, cpf_cnpj)],
            NOME_SOCIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, nome_social)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            CONFIRMAR_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar_email)],
            TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, telefone)],
            WHATSAPP: [MessageHandler(filters.TEXT & ~filters.COMMAND, whatsapp)],
            CEP: [MessageHandler(filters.TEXT & ~filters.COMMAND, cep)],
            LOGRADOURO: [MessageHandler(filters.TEXT & ~filters.COMMAND, logradouro)],
            NUMERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, numero)],
            COMPLEMENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, complemento)],
            BAIRRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bairro)],
            CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cidade)],
            UF: [MessageHandler(filters.TEXT & ~filters.COMMAND, uf)],
            CONFIRMAR_CADASTRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar_cadastro)],
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nome)],
            DATA_COMPRA: [MessageHandler(filters.TEXT & ~filters.COMMAND, data_compra)],
            PRODUTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, produto)],
            MARCA: [MessageHandler(filters.TEXT & ~filters.COMMAND, marca)],
            VALOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, valor)],
            LOJA: [MessageHandler(filters.TEXT & ~filters.COMMAND, loja)],
            ORDEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ordem)],
            DATA_ORDEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, data_ordem)],
            VALOR_INDEMNIZACAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, valor_indenizacao)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
