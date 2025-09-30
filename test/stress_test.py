import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import multiprocessing
import socket
import time
from config import HOST, PORT
from utils import format_message

def simulate_client(name, message):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.send(name.encode())
        time.sleep(1)
        formatted = format_message(name, message)
        client.send(formatted.encode())
        time.sleep(2)
        client.close()
    except Exception as e:
        print(f"[Erro] Cliente {name}: {e}")

if __name__ == "__main__":
    clients = []
    for i in range(10):
        name = f"Bot{i}"
        msg = f"Olá, sou o {name}"
        p = multiprocessing.Process(target=simulate_client, args=(name, msg))
        clients.append(p)
        p.start()

    for p in clients:
        p.join()
