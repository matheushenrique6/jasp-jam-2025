import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler,ApplicationBuilder
from chatbot.collector import QueixaOxidacaoData
from chatbot.formatter import gerar_peticao_oxidacao
from config import TELEGRAM_TOKEN
from chatbot.pdf_generator import gerar_pdf
logging.basicConfig(level=logging.INFO)

# Estados da conversa
NOME, DATA_COMPRA, PRODUTO, MARCA, VALOR, LOJA, ORDEM, DATA_ORDEM, VALOR_INDEMNIZACAO = range(9)
user_data_dict = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Vou ajudá-lo a criar sua queixa de vício do produto. Qual seu nome?")
    return NOME

async def nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id] = QueixaOxidacaoData(nome_autor=update.message.text)
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
    
    # Gera a petição refinada pelo Gemini
    peticao = gerar_peticao_oxidacao(user_data_dict[user_id])
    
    # Gera PDF
    arquivo_pdf = gerar_pdf(peticao, nome_arquivo=f"peticao_{user_id}.pdf")
    
    # Envia mensagem com PDF
    with open(arquivo_pdf, "rb") as f:
        await update.message.reply_document(document=f, filename=arquivo_pdf, caption="Sua petição está pronta!")
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operação cancelada.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
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
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
