from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import telebot
import pickle
import csv

"""def save_update(update):
    #Salva os dados Update para ser usado por outras funções.
    with open("update.pickle", "wb") as f:
        pickle.dump(update, f)

async def open_update():
    with open("update.pickle", "rb") as f:
        update = pickle.load(f)
    print(update)
    return update"""
def abrir_matriz():
    matriz=[]
    with open("dados.csv","r") as arquivo:
        arquivo_csv=csv.reader(arquivo,delimiter=",")
        for i, linha in enumerate(arquivo_csv):
            matriz.append(linha)
        return matriz
def salvar_matriz(matriz):
    with open("dados.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(matriz)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    #save_update(update)
    user = update.effective_user
    nome_jogador=user["first_name"]
    print(update)
    verificar_usuario(nome_jogador,update.message.chat.id)
    await update.message.reply_html(rf"Hi {user.mention_html()}!",reply_markup=ForceReply(selective=False))
def verificar_usuario(nome,id):
    matriz=abrir_matriz()
    #print(matriz)

    if matriz[0].count(nome) == 0:
        #Criar o jogador e dados de conquistas
        matriz[0].append(nome)
        matriz[1].append(id)
        matriz[2].append("AA0")

        #Salvar alterações feitas
        salvar_matriz(matriz)

        #Chamar apresentação sobre o jogo
        apresentacao(nome,id)

    elif matriz[0].count(nome) == 1:
        #Indentificar o jogador.

        #Informar que o jogador ja tem um jogo em aberto, perguntar se ele que reiniciar ou continuar daonde parou.

        x=0
    else:
        #Informar que ocorreu um erro, que usuario esta duplicado e procurar o suporte.
        x=0


def apresentacao(nome,id):
    telebot.TeleBot("6221766418:AAELMn98mvk8Pk2m2zn7wPF97D9B3OezvBU").send_message(id, f'Ola {nome}, esse é um projeto...')