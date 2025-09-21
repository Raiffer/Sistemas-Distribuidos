import socket
import threading
import json
from leitor import Leitor

HOST = "127.0.0.1"
PORT = 5000
leitor = Leitor()

def receber(conn):
    while True:
        header = conn.recv(10).decode("utf-8")
        if not header:
            break
        tamanho = int(header)

        recebido = 0
        dados = []
        while recebido < tamanho:
            parte = conn.recv(4096)
            if not parte:
                break
            dados.append(parte)
            recebido += len(parte)

        conteudo = b"".join(dados).decode("utf-8")
        leitor.ler_mensagem(conteudo)

def cliente(meu_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    sock.send(f"{meu_id:<20}".encode("utf-8"))

    threading.Thread(target=receber, args=(sock,), daemon=True).start()

    while True:
        destinatario = input("Destinatario: ")
        mensagem = input("Escreva sua mensagem: ")
        arquivo = leitor.criar_mensagem(destinatario, mensagem, meu_id)
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        tamanho = len(conteudo.encode("utf-8"))

        sock.send(f"{tamanho:010}".encode("utf-8"))
        sock.send(conteudo.encode("utf-8"))

if __name__ == "__main__":
    meu_id = input("Digite seu ID: ")
    cliente(meu_id)
