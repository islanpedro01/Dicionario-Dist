import socket
import threading

HOST = 'localhost'
PORT = 5000

dicionario = {}
lock = threading.Lock()

def tratar_cliente(conn, addr):
    print(f"[+] Conexão de {addr}")
    try:
        with conn:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                partes = data.strip().split()
                if len(partes) < 2:
                    conn.sendall(b'Erro: comando invalido\n')
                    continue

                comando = partes[0].lower()
                chave = partes[1]

                if comando == 'update':
                    if len(partes) != 3 or not partes[2].isdigit():
                        conn.sendall(b'Erro: uso correto update <chave> <valor>\n')
                        continue
                    valor = int(partes[2])
                    with lock:
                        nova = chave not in dicionario
                        dicionario[chave] = valor
                    conn.sendall(f"{nova}\n".encode())

                elif comando == 'remove':
                    with lock:
                        removido = dicionario.pop(chave, None) is not None
                    conn.sendall(f"{removido}\n".encode())

                elif comando == 'get':
                    with lock:
                        valor = dicionario.get(chave, -1)
                    conn.sendall(f"{valor}\n".encode())

                else:
                    conn.sendall(b'Erro: comando desconhecido\n')
    finally:
        print(f"[-] Conexao encerrada de {addr}")

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Servidor escutando em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=tratar_cliente, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    iniciar_servidor()
