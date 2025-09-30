import socket
import threading
import json
import logging
import os
from datetime import datetime
from config import HOST, PORT, MAX_CLIENTS, ADMIN_USER
from utils import format_message, validate_message

clients = {}
lock = threading.Lock()

# Configura o log
logging.basicConfig(filename='logs/server.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def broadcast(message, sender_socket):
    with lock:
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    logging.error(f"Erro ao enviar mensagem: {e}")
                    client_socket.close()
                    del clients[client_socket]

def handle_client(client_socket, addr):
    try:
        username = client_socket.recv(1024).decode()
        with lock:
            clients[client_socket] = username
        logging.info(f"{username} conectado de {addr}")
        welcome = format_message("Servidor", f"{username} entrou no chat.")
        broadcast(welcome, client_socket)

        while True:
            raw_msg = client_socket.recv(1024).decode()
            if not raw_msg:
                break
            if validate_message(raw_msg):
                msg_data = json.loads(raw_msg)
                content = msg_data["message"]

                if content == "/encerrar" and username == ADMIN_USER:
                    broadcast(format_message("Servidor", "Servidor encerrado pelo administrador."), None)
                    logging.info("Servidor encerrado remotamente pelo administrador.")
                    os._exit(0)  # Encerra o processo imediatamente
                else:
                    formatted = format_message(username, content)
                    broadcast(formatted, client_socket)
            else:
                logging.warning(f"Mensagem inválida de {username}: {raw_msg}")
    except Exception as e:
        logging.error(f"Erro com cliente {addr}: {e}")
    finally:
        with lock:
            left_user = clients.get(client_socket, "Desconhecido")
            del clients[client_socket]
        client_socket.close()
        logging.info(f"{left_user} desconectado.")
        broadcast(format_message("Servidor", f"{left_user} saiu do chat."), None)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)
    logging.info(f"Servidor iniciado em {HOST}:{PORT}")
    print(f"[Servidor] Rodando em {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            if len(clients) >= MAX_CLIENTS:
                client_socket.send("Servidor cheio.".encode())
                client_socket.close()
                continue
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[Servidor] Encerrando manualmente...")
        logging.info("Servidor encerrado manualmente com Ctrl+C.")
        server.close()
        for client in clients:
            client.close()
        print("[Servidor] Todos os sockets foram fechados.")


if __name__ == "__main__":
    start_server()
