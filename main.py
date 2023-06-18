from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import func
def main() -> None:

    with open('token.txt', 'r') as arquivo:
         token = arquivo.read()

    application = Application.builder().token(token).build()

    # Comandos recebidos pelo CommandHandler e qual função ele deve chamar.
    application.add_handler(CommandHandler("start", func.start))

    application.add_handler(CommandHandler("1", func.op))
    application.add_handler(CommandHandler("2", func.op))
    application.add_handler(CommandHandler("3", func.op))
    application.add_handler(CommandHandler("4", func.op))
    application.add_handler(CommandHandler("novo", func.novo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()