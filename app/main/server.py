import socket
from app.algorithm.diffie_hellman import DiffieHellman
from app.algorithm.caesar_cipher import Caesar


class Server:
    secret_key = None

    def __init__(self, sock):
        self.socket = sock
        data = self.socket.recv(1024)
        shared_numbers = data.split()
        shared_base = int(shared_numbers[0])
        shared_prime = int(shared_numbers[1])

        diffie_hellman = DiffieHellman()
        private_key = diffie_hellman.generate_private_key()
        public_key = diffie_hellman.generate_public_key(private_key, shared_prime, shared_base)

        self.socket.send(str.encode(str(public_key)))
        data = self.socket.recv(1024)
        client_public_key = int(data.decode())
        self.secret_key = diffie_hellman.retrieve_secret_key(client_public_key, private_key, shared_prime)


def server():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 3000))
    sock.listen(1)
    conn, addr = sock.accept()

    server_obj = Server(conn)
    server_secret_key = server_obj.secret_key
    print("Server secret key: ", server_secret_key)

    caesar = Caesar(server_secret_key)

    data = conn.recv(1024)
    while data:
        received_message = data.decode()
        print("Received message from client:", received_message)
        caesar.decrypt_text(data.decode(), server_obj.secret_key)
        data = conn.recv(1024)

    conn.close()


if __name__ == "__main__":
    server()
