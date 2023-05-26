from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import func

#Codigo para o GPT responder via telegram, ele guarda as 2 ultimas interações, ou seja, 4 ultimas msgs.
#Sem usar comando ele se limita a 500Tokens, usando o comando ele pode ir ate 3k de tokens.


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    with open('token.txt', 'r') as arquivo:
         token = arquivo.read()

    application = Application.builder().token(token).build()

    # Comandos recebidos pelo CommandHandler e qual função ele deve chamar.
    application.add_handler(CommandHandler("start", func.start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("1", func.op))
    application.add_handler(CommandHandler("2", func.op))
    application.add_handler(CommandHandler("3", func.op))
    application.add_handler(CommandHandler("4", func.op))
    application.add_handler(CommandHandler("novo", func.novo))

    # on non command i.e message - echo the message on Telegram

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()