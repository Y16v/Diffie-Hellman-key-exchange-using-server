import socket
from app.algorithm.diffie_hellman import DiffieHellman
from app.algorithm.caesar_cipher import Caesar


class Client:
    secret_key = None

    def __init__(self, sock):
        self.socket = sock

        diffie_hellman = DiffieHellman()
        primes = diffie_hellman.create_possible_primes()
        shared_prime = diffie_hellman.generate_shared_prime(primes)
        shared_base = diffie_hellman.generate_shared_base(primes)
        private_key = diffie_hellman.generate_private_key()
        public_key = diffie_hellman.generate_public_key(private_key, shared_prime, shared_base)

        self.socket.send(str.encode(str(shared_base) + " " + str(shared_prime)))
        data = self.socket.recv(1024)

        server_public_key = int(data.decode())
        self.socket.send(str.encode(str(public_key)))
        self.secret_key = diffie_hellman.retrieve_secret_key(server_public_key, private_key, shared_prime)


def client():
    sock = socket.socket()
    sock.connect(('127.0.0.1', 3000))

    client_obj = Client(sock)
    client_secret_key = client_obj.secret_key
    print("Client secret key:", client_secret_key)

    caesar = Caesar(client_secret_key)

    # start sending messages
    message = input("Message: ")
    while message != "quit":
        cipher_text = caesar.encrypt_text(message, client_obj.secret_key)
        sock.send(str.encode(cipher_text))
        message = input("Message: ")

    sock.close()


if __name__ == "__main__":
    client()
