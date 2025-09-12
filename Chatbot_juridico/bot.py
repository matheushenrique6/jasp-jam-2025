import logging
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
from config import TELEGRAM_TOKEN

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
# Fluxo de cadastro do demandante
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Vamos começar cadastrando seus dados.\nQual seu nome completo?")
    return NOME_DEMANDANTE

async def nome_demandante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id] = QueixaOxidacaoData()
    user_data_dict[user_id].nome_demandante = update.message.text
    await update.message.reply_text("CPF/CNPJ *")
    return CPF_CNPJ

async def cpf_cnpj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].cpf_cnpj = update.message.text
    await update.message.reply_text("Nome Social (opcional)")
    return NOME_SOCIAL

async def nome_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].nome_social = update.message.text
    await update.message.reply_text("E-mail *")
    return EMAIL

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].email = update.message.text
    await update.message.reply_text("Confirme seu e-mail *")
    return CONFIRMAR_EMAIL

async def confirmar_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].confirmar_email = update.message.text
    await update.message.reply_text("Telefone *")
    return TELEFONE

async def telefone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].telefone = update.message.text
    await update.message.reply_text("Este telefone possui Whatsapp? (sim/não)")
    return WHATSAPP

async def whatsapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].whatsapp = update.message.text
    await update.message.reply_text("CEP")
    return CEP

async def cep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].cep = update.message.text
    await update.message.reply_text("Logradouro *")
    return LOGRADOURO

async def logradouro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].logradouro = update.message.text
    await update.message.reply_text("Número *")
    return NUMERO

async def numero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].numero = update.message.text
    await update.message.reply_text("Complemento (opcional)")
    return COMPLEMENTO

async def complemento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].complemento = update.message.text
    await update.message.reply_text("Bairro *")
    return BAIRRO

async def bairro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].bairro = update.message.text
    await update.message.reply_text("Cidade *")
    return CIDADE

async def cidade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].cidade = update.message.text
    await update.message.reply_text("UF *")
    return UF

async def uf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].uf = update.message.text
    await update.message.reply_text(
        "Declaro que resido no endereço informado. \nDigite 'ok' para confirmar e continuar com a queixa."
    )
    return CONFIRMAR_CADASTRO

async def confirmar_cadastro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cadastro concluído! Agora vamos à queixa do produto.\nQual o seu nome?")
    return NOME

# --------------------------
# Fluxo de queixa
# --------------------------
async def nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].nome_autor = update.message.text
    await update.message.reply_text("Data da compra? (dd/mm/aaaa)")
    return DATA_COMPRA

async def data_compra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].data_compra = update.message.text
    await update.message.reply_text("Qual o produto comprado?")
    return PRODUTO

async def produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].produto = update.message.text
    await update.message.reply_text("Qual a marca do produto?")
    return MARCA

async def marca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].marca = update.message.text
    await update.message.reply_text("Qual o valor pago?")
    return VALOR

async def valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].valor_pago = float(update.message.text.replace(",", "."))
    await update.message.reply_text("Qual a loja onde comprou?")
    return LOJA

async def loja(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].loja = update.message.text
    await update.message.reply_text("Número da ordem de serviço?")
    return ORDEM

async def ordem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].ordem_servico = update.message.text
    await update.message.reply_text("Data da ordem de serviço? (dd/mm/aaaa)")
    return DATA_ORDEM

async def data_ordem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].data_ordem_servico = update.message.text
    await update.message.reply_text("Valor da indenização desejada?")
    return VALOR_INDEMNIZACAO

async def valor_indenizacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id].valor_indenizacao = float(update.message.text.replace(",", "."))

    peticao = gerar_peticao_oxidacao(user_data_dict[user_id])
    arquivo_pdf = gerar_pdf(
        user_data_dict[user_id].dict(),  # dados cadastrais
        peticao,                        # texto da petição
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
    await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END

# --------------------------
# Main
# --------------------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # Cadastro
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

            # Queixa
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
