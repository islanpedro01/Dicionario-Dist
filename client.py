import socket

HOST = 'localhost'
PORT = 5000

def cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Digite comandos: update <chave> <valor> | get <chave> | remove <chave>")
        while True:
            cmd = input("> ")
            if cmd.strip().lower() in ['sair', 'exit', 'quit']:
                break
            s.sendall(cmd.encode())
            resposta = s.recv(1024).decode()
            print("Resposta:", resposta.strip())

if __name__ == "__main__":
    cliente()
