import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5000

clientes = {} 

def tratar_cliente(conn, addr):
    try:
        cliente_id = conn.recv(20).decode("utf-8").strip()
        clientes[cliente_id] = conn
        print(f"Cliente {cliente_id} conectado de {addr}")

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

            try:
                json_obj = json.loads(conteudo)
                dest_id = json_obj.get("destinatario")
            except Exception as e:
                print(f"Erro ao processar JSON: {e}")
                continue

            if dest_id in clientes:
                print(f"Repassando arquivo de {cliente_id} para {dest_id}")
                clientes[dest_id].send(f"{tamanho:010}".encode("utf-8"))
                clientes[dest_id].send(conteudo.encode("utf-8"))
            else:
                print(f"Destinatário {dest_id} não está online")
    except:
        pass
    finally:
        conn.close()
        if cliente_id in clientes:
            del clientes[cliente_id]
        print(f"Cliente {cliente_id} desconectado")

def servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Servidor ouvindo em {HOST}:{PORT}")

    while True:
        conn, addr = sock.accept()
        threading.Thread(target=tratar_cliente, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    servidor()
