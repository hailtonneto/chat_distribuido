import socket
import threading
import json
from datetime import datetime
from config import HOST, PORT
from utils import format_message

def receive_messages(client_socket):
    while True:
        try:
            raw_msg = client_socket.recv(1024).decode()
            if raw_msg:
                msg_data = json.loads(raw_msg)
                print(f"[{msg_data['timestamp']}] {msg_data['sender']}: {msg_data['message']}")
            else:
                break
        except:
            print("[Erro] Conexão encerrada pelo servidor.")
            client_socket.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    username = input("Digite seu nome de usuário: ")
    client.send(username.encode())

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    print("Você entrou no chat. Digite suas mensagens abaixo:")
    while True:
        try:
            msg = input()
            if msg.lower() == "/sair":
                client.close()
                break
            formatted = format_message(username, msg)
            client.send(formatted.encode())
        except:
            print("[Erro] Falha ao enviar mensagem.")
            client.close()
            break

if __name__ == "__main__":
    start_client()
