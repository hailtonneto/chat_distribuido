import socket
import threading
import json
import logging
import os
from datetime import datetime
from config import HOST, PORT, MAX_CLIENTS, ADMIN_USER, ADMIN_PASSWORD
from utils import format_message, validate_message

clients = {}
lock = threading.Lock()

# Configura o log
logging.basicConfig(filename='logs/server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def broadcast(message, sender_socket):
    desconectar = []
    with lock:
        for client_socket in list(clients):
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    logging.error(f"Erro ao enviar mensagem: {e}")
                    desconectar.append(client_socket)
        for sock in desconectar:
            sock.close()
            clients.pop(sock, None)

def handle_client(client_socket, addr):
    try:
        auth_raw = client_socket.recv(1024).decode()
        try:
            auth_data = json.loads(auth_raw)
            username = auth_data.get("username")
            password = auth_data.get("password")
        except (json.JSONDecodeError, AttributeError):
            client_socket.send("Erro na autenticação. Dados inválidos.".encode())
            client_socket.close()
            return

        if not username:
            client_socket.send("Nome de usuário inválido.".encode())
            client_socket.close()
            return

        if username == ADMIN_USER and password != ADMIN_PASSWORD:
            client_socket.send("Senha incorreta para administrador.".encode())
            client_socket.close()
            return

        with lock:
            clients[client_socket] = username
        logging.info(f"{username} conectado de {addr}")
        broadcast(format_message("Servidor", f"{username} entrou no chat."), client_socket)

        while True:
            raw_msg = client_socket.recv(1024).decode()
            if not raw_msg:
                break
            if not validate_message(raw_msg):
                logging.warning(f"Mensagem inválida de {username}: {raw_msg}")
                continue

            msg_data = json.loads(raw_msg)
            content = msg_data["message"]

            if content == "/encerrar" and username == ADMIN_USER:
                broadcast(format_message("Servidor", "Servidor encerrado pelo administrador."), None)
                logging.info("Servidor encerrado remotamente pelo administrador.")
                os._exit(0)

            if content == "/limparlog" and username == ADMIN_USER:
                try:
                    with open("logs/server.log", "w") as log_file:
                        log_file.write("")
                    logging.info("Log do servidor foi limpo pelo administrador.")
                    broadcast(format_message("Servidor", "Log do servidor foi limpo pelo administrador."), None)
                except Exception as e:
                    logging.error(f"Erro ao limpar log: {e}")
                continue

            if content in ["/encerrar", "/limparlog"]:
                logging.warning(f"Usuário não autorizado tentou usar comando: {username} → {content}")
                continue

            broadcast(format_message(username, content), client_socket)

    except Exception as e:
        logging.error(f"Erro com cliente {addr}: {e}")
    finally:
        with lock:
            left_user = clients.pop(client_socket, "Desconhecido")
        client_socket.close()
        logging.info(f"{left_user} desconectado.")
        broadcast(format_message("Servidor", f"{left_user} saiu do chat."), None)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)
    server.settimeout(1.0)
    logging.info(f"Servidor iniciado em {HOST}:{PORT}")
    print(f"[Servidor] Rodando em {HOST}:{PORT}")

    while True:
        try:
            client_socket, addr = server.accept()
        except socket.timeout:
            continue

        if client_socket:
            if len(clients) >= MAX_CLIENTS:
                client_socket.send("Servidor cheio.".encode())
                client_socket.close()
                continue
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
