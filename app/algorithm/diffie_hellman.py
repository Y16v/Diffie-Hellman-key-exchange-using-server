import random


class DiffieHellman:

    def __init__(self):
        self.lower_bound = 2
        self.upper_bound = 26
        self.primes = []

    def create_possible_primes(self):
        for possible_prime in range(self.lower_bound, self.upper_bound):
            is_prime = True
            for num in range(self.lower_bound, possible_prime):
                if possible_prime % num == 0:
                    is_prime = False
                    break
            if is_prime:
                self.primes.append(possible_prime)
        print("Primes list:", self.primes)
        return self.primes

    def generate_shared_prime(self, primes):
        shared_prime = random.choice(primes)  # p
        print("Publicly Shared Prime:", shared_prime)
        return shared_prime

    def generate_shared_base(self, primes):
        shared_base = random.choice(primes)  # g
        print("Publicly Shared Base:", shared_base)
        return shared_base

    def generate_private_key(self):
        private_key = random.randint(2, 100)
        print("Private key:", private_key)
        return private_key

    def generate_public_key(self, private_key, shared_prime, shared_base):
        public_key = (shared_base ** private_key) % shared_prime
        print("Sends Over Public Chanel:", public_key)
        return public_key

    def retrieve_secret_key(self, public_key, private_key, shared_prime):
        secret_key = (public_key ** private_key) % shared_prime
        print("Secret key:", secret_key)
        return secret_key

