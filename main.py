from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import pickle

#Codigo para o GPT responder via telegram, ele guarda as 2 ultimas interações, ou seja, 4 ultimas msgs.
#Sem usar comando ele se limita a 500Tokens, usando o comando ele pode ir ate 3k de tokens.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    with open('lista.pickle', 'rb') as f:
        messages = pickle.load(f)

    messages=[{"role": "system", "content": "Fale apenas a verdade."}]

    with open('lista.pickle', 'wb') as f:
        pickle.dump(messages, f)

    await update.message.reply_text("Help!")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6221766418:AAELMn98mvk8Pk2m2zn7wPF97D9B3OezvBU").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()