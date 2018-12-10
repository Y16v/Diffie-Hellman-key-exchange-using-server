class Caesar:
    secret_key = None
    l2i = None
    i2l = None

    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.l2i = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
        self.i2l = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    def set_secret_key(self, secret_key):
        self.secret_key = secret_key

    def encrypt_text(self, plain_text, secret_key):
        encrypted_text = ""
        for char in plain_text.upper():
            if char.isalpha():
                encrypted_text += self.i2l[(self.l2i[char] + secret_key) % 26]
            else:
                encrypted_text += char
        print("Encrypted message:", encrypted_text)
        return encrypted_text

    def decrypt_text(self, encrypted_text, secret_key):
        decrypted_text = ""
        for char in encrypted_text.upper():
            if char.isalpha():
                decrypted_text += self.i2l[(self.l2i[char] - secret_key) % 26]
            else:
                decrypted_text += char
        print("Decrypted message:", decrypted_text)
        return decrypted_text

