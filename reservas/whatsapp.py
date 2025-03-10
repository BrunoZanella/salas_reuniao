import requests
import json
from django.conf import settings
import time
import threading

def enviar_mensagem_whatsapp(telefone, mensagem):
    """
    Envia uma mensagem via WhatsApp usando a Evolution API.
    
    Args:
        telefone (str): Número de telefone do destinatário (com ou sem o prefixo 55)
        mensagem (str): Texto da mensagem a ser enviada
    """
    # Garante que o telefone tenha o formato correto
    telefone = ''.join(filter(str.isdigit, telefone))
    if not telefone.startswith('55'):
        telefone = f"55{telefone}"
    
    print(f"Enviando mensagem para {telefone}")
    
    url = f"{settings.EVOLUTION_API_URL}/message/sendText/{settings.EVOLUTION_API_INSTANCE}"
    headers = {
        "Content-Type": "application/json",
        "apikey": settings.EVOLUTION_API_KEY
    }
    payload = {
        "number": telefone,
        "options": {
            "delay": 1200,
            "presence": "composing",
            "linkPreview": False
        },
        "textMessage": {
            "text": mensagem
        }
    }
    
    try:
        # Adiciona um pequeno atraso para evitar sobrecarga da API
        time.sleep(1)
        
        # Faz a requisição com timeout de 30 segundos
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()
        
        # Tenta converter a resposta para JSON
        response_json = response.json()
        return response_json
    except Exception as e:
        print(f"Erro ao enviar mensagem WhatsApp: {str(e)}")
        # Não propaga o erro para não afetar o fluxo principal

def async_enviar_mensagens_whatsapp(contatos, mensagem):
    """
    Envia mensagens WhatsApp de forma assíncrona usando threads.
    
    Args:
        contatos (list): Lista de objetos ContatoWhatsApp
        mensagem (str): Mensagem a ser enviada
    """
    def worker():
        for contato in contatos:
            try:
                enviar_mensagem_whatsapp(contato.telefone, mensagem)
            except Exception as e:
                print(f"Erro ao enviar mensagem para {contato.telefone}: {str(e)}")
                continue
    
    # Inicia uma nova thread para enviar as mensagens
    thread = threading.Thread(target=worker)
    thread.daemon = True  # A thread será encerrada quando o programa principal terminar
    thread.start()