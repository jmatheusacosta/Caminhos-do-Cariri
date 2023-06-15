from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import telebot
import csv, token

def abrir_dados():
    matriz=[]
    with open("dados.csv","r",encoding='utf-8') as arquivo:
        arquivo_csv=csv.reader(arquivo,delimiter=",")
        for i, linha in enumerate(arquivo_csv):
            matriz.append(linha)
        return matriz
def salvar_dados(matriz):
    with open("dados.csv", "w",encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(matriz)
def abrir_caminhos():
    caminhos=[]
    with open("caminhos.csv","r",encoding='utf-8') as arquivo:
        arquivo_csv=csv.reader(arquivo,delimiter=",")
        for i, linha in enumerate(arquivo_csv):
            caminhos.append(linha)
        return caminhos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #obtem dados de quem entrou em contato com o bot
    user = update.effective_user
    nome_jogador=update.effective_user.first_name
    #Verifica se é um novo ou antigo jogador
    stats_jogador=verificar_usuario(nome_jogador,update.message.chat.id)


    #Reage baseado na situação do jogador
    if stats_jogador==0:
        pergunta=caminho_atual(nome_jogador)
        await update.message.reply_html(rf"{pergunta}")
    elif stats_jogador==1:
        await update.message.reply_html(rf"Você tem um jogo em aberto, continue ele ou digite /novo para começar um novo jogo.")
        pergunta = caminho_atual(nome_jogador)
        await update.message.reply_html(rf"{pergunta}")
    else:
        await update.message.reply_html(rf"Ola, um erro (ZX7) foi encontrado, se possivel entre em contato com o suporte para resolver essa situação!")
def verificar_usuario(nome,id):
    matriz=abrir_dados()
    #print(matriz)

    if matriz[0].count(nome) == 0:
        #Criar o jogador e dados de conquistas
        matriz[0].append(nome)
        matriz[1].append(id)
        matriz[2].append("0")#Alterar futuramente para a pergunta inicial

        #Salvar alterações feitas
        salvar_dados(matriz)

        #Chamar apresentação sobre o jogo
        apresentacao(nome,id)

        #Informa que o usuario é novo, e inicia a primeira pergunta
        return 0

    elif matriz[0].count(nome) == 1:
        #Informar que o jogador ja tem um jogo em aberto, perguntar se ele que reiniciar ou continuar daonde parou.

        return 1
    else:
        #Informar que ocorreu um erro, que usuario esta duplicado e procurar o suporte.
        return 2
def apresentacao(nome,id):
    telebot.TeleBot("6221766418:AAELMn98mvk8Pk2m2zn7wPF97D9B3OezvBU").send_message(id, f'Ola {nome}, "Caminhos do Cariri", é uma história interativa feita pela 2JD como um projeto sustentado por um código que permite a criação e implementaçãode outras histórias com temáticas diferentes, esta aqui, visa despertar a curiosidade e o interesse de seus usuários em explorar as maravilhasdo estado do Ceará, mais especificamente, a região do Crajubar. \n\n O jogo é cuidadosamente projetado para oferecer uma experiência turísticaimersiva, apresentando locais reais do estado do Ceará. "Caminhos do Cariri" tem como objetivo não apenas entreter, mas também educar eincentivar as pessoas a explorarem o estado do Ceará de forma real e virtual. \n\n Ao jogar, os participantes serão incentivados a refletir sobresuas escolhas e como elas podem impactar a sua experiência na região que estão visitando. \n\n Uma jogabilidade envolvente e simples,"Caminhos do Cariri" é um convite para os viajantes e romeiros, e incita os curiosos de plantão a descobrirem o estado do Ceará de uma maneiratotalmente nova pela visão dos locais....')
async def novo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matriz = abrir_dados()

    # Encontra o nome do jogador
    nome_jogador = update.effective_user.first_name
    #Encontra a posição do jogador na planilha
    id_jogador = matriz[0].index(nome_jogador)
    matriz[2][id_jogador]="0"

    salvar_dados(matriz)
    pergunta = caminho_atual(nome_jogador)
    await update.message.reply_html(rf"{pergunta}")

async def foto(update: Update, context):
    photo_path = 'teste.jpg'

    # Texto a ser enviado junto com a foto
    caption = 'Aqui está a foto de teste!'

    # Envio da foto com o texto para o usuário
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photo_path, 'rb'), caption=caption)


def caminho_atual(nome_jogador):
    # Extrai os dados de jogador do CSV
    matriz = abrir_dados()
    # Encontra a posição do jogador na planilha
    id_jogador = matriz[0].index(nome_jogador)
    # Usa o ID do jogador para saber qual o ID da pergunta que o jogador parou.
    id_caminho_atual = (matriz[2][id_jogador])

    # Extrai os dados dos Caminhos do CSV
    caminhos = abrir_caminhos()
    # Indentifica o Caminho em que o jogador parou, basedo no ID da pergunta obtido anteriomente
    id_caminho = caminhos[0].index(id_caminho_atual)

    texto_caminho=caminhos[1][id_caminho]

    for c in range(0,int(caminhos[6][id_caminho])):
        texto_caminho=texto_caminho+'\n\n'+caminhos[7+(2*c)][id_caminho]
        #print(caminhos[5+(2*c)][id_caminho])
    texto_caminho=texto_caminho.replace('/n','\n')
    return texto_caminho
async def op(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #Retirar do Update qual opção o usruaio escolheu.
    escolha=int((update.message.text[1]))

    #Extrai os dados de jogador do CSV
    matriz=abrir_dados()
    print(matriz)
    # Encontra o nome do jogador
    nome_jogador = update.effective_user.first_name
    #Encontra a posição do jogador na planilha
    id_jogador = matriz[0].index(nome_jogador)
    #Usa o ID do jogador para saber qual o ID da pergunta que o jogador parou.
    id_caminho_atual = (matriz[2][id_jogador])

    #Extrai os dados dos Caminhos do CSV
    caminhos = abrir_caminhos()
    #Indentifica o Caminho em que o jogador parou, basedo no ID da pergunta obtido anteriomente
    id_caminho = caminhos[0].index(id_caminho_atual)

    #Verifica se na pergunta atual existe a opção selecionada pelo jogador
    if escolha>int(caminhos[6][id_caminho]):
        texto_caminho=caminho_atual(nome_jogador)
        await update.message.reply_html(rf"Opção invalida, releia com atenção e escolha uma opção valida.")
        await update.message.reply_html(rf"{texto_caminho}")

    else:
        #Encontra o ID do proximo caminho escolhido pelo usuario
        id_proximo_caminho=caminhos[6+(2*escolha)][id_caminho]

        #Altera na planilha de dados o ID do caminho que o usuario se encontra para o caminho escolhido.
        matriz[2][id_jogador] = id_proximo_caminho
        salvar_dados(matriz)

        pergunta=caminho_atual(nome_jogador)

        # Extrai os dados de jogador do CSV
        matriz = abrir_dados()
        print(matriz)

        # Atualiza informações caso va ser mandado foto
        nome_jogador = update.effective_user.first_name
        id_jogador = matriz[0].index(nome_jogador)
        id_caminho_atual = (matriz[2][id_jogador])
        caminhos = abrir_caminhos()
        id_caminho = caminhos[0].index(id_caminho_atual)

        #print(id_caminho)
        #print(caminhos[2][id_caminho])
        if caminhos[2][id_caminho]=='true':
            try:
                nome_foto=caminhos[3][id_caminho]
                local_foto="imagens/"+nome_foto+".jpg"
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(local_foto, 'rb'), caption=pergunta)
            except:
                print('erro')
                await update.message.reply_html(rf"{pergunta}")
        else:
            await update.message.reply_html(rf"{pergunta}")
