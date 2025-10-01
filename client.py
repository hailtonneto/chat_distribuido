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
            if not raw_msg:
                break
            msg_data = json.loads(raw_msg)
            print(f"[{msg_data['timestamp']}] {msg_data['sender']}: {msg_data['message']}")
        except Exception:
            print("[Erro] Conexão encerrada pelo servidor.")
            break
    try:
        client_socket.close()
    except:
        pass

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        print(f"[Erro] Falha ao conectar ao servidor: {e}")
        return

    username = input("Digite seu nome de usuário: ")
    if not username:
        print("Nome de usuário não pode ser vazio.")
        return

    password = input("Digite a senha do administrador: ") if username == "admin" else ""

    auth_data = json.dumps({"username": username, "password": password})
    client.send(auth_data.encode())

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.daemon = True
    thread.start()

    print("Você entrou no chat. Digite suas mensagens abaixo:")
    while True:
        try:
            msg = input()
            if msg.lower() == "/sair":
                break
            formatted = format_message(username, msg)
            client.send(formatted.encode())
        except Exception:
            print("[Erro] Falha ao enviar mensagem.")
            break
    try:
        client.close()
    except:
        pass

if __name__ == "__main__":
    start_client()
