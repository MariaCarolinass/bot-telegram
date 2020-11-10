from flask import Flask, request
import requests
import random

app = Flask(__name__)

BOT_TOKEN = "SEU_TOKEN" # Não compartilhar Token

@app.route('/nova-mensagem', methods=["POST"])
def nova_mensagem():
    mensagem = request.json # pegar a mensagem que o telegram enviou
    app.logger.info(f"Chegou uma nova mensagem: {mensagem}")
    resposta = montar_resposta(mensagem) # escolher um texto de resposta para a mensagem recebida
    enviar_mensagem(resposta, mensagem) # enviar mensagem respondendo o usuário
    return {"ok": True} # falar para o telegram que tudo ocorreu bem

def montar_resposta(mensagem):
    if 'text' in mensagem['message']:
        texto_recebido = mensagem['message']['text']
        nome_usuario = mensagem['message']['from']['first_name']
        frutas = [
                'banana','maçã','uva','abacaxi', 'morango', 'pera', 'melancia',
                'abacate', 'laranja', 'Goiaba', 'Pêssego', 'caju', 'mamão', 'melão'
                ]
        sorteador = random.choice(frutas)
        if texto_recebido != '/start':
            return (
                f"Olá, {nome_usuario}!\n\n"
                f"Fruta sorteada: *{sorteador}*"
            )
        return (
            "Sou um bot sorteador de frutas!\n\n"
            "Digite 1 que sortearei uma fruta."
        )
    else:
        return "Inválido"

def enviar_mensagem(texto, mensagem):
    endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": mensagem['message']['chat']['id'],
        "text": texto,
    }
    requests.get(endpoint, params)
