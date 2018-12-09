#Diffie-Hellman
import random
primes = []
for possiblePrime in range(2, 26):

    isPrime = True
    for num in range(2, possiblePrime):
        if possiblePrime % num == 0:
            isPrime = False
            break

    if isPrime:
        primes.append(possiblePrime)


sharedPrime = random.choice(primes)  # p
sharedBase = random.choice(primes)  # g

clientSecret = random.randint(3,26)  # a
serverSecret = random.randint(4,26)  # b


print("    Publicly Shared Prime: ", sharedPrime)
print("    Publicly Shared Base:  ", sharedBase)


A = (sharedBase ** clientSecret) % sharedPrime
print("\n  client Sends Over Public Chanel: ", A)


B = (sharedBase ** serverSecret) % sharedPrime
print("server Sends Over Public Chanel: ", B )

clientSharedSecret = (B ** clientSecret) % sharedPrime

serverSharedSecret = (A ** serverSecret) % sharedPrime


#Ceaser Cipher

L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",range(26)))
I2L = dict(zip(range(26),"ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

key = serverSharedSecret
plaintext = input("Please input your plain text: ")

# encipher
ciphertext = ""
for c in plaintext.upper():
    if c.isalpha(): ciphertext += I2L[ (L2I[c] + key)%26 ]
    else: ciphertext += c

# decipher
decryptedText = ""
for c in ciphertext.upper():
    if c.isalpha(): decryptedText += I2L[ (L2I[c] - key)%26 ]
    else: decryptedText += c


print (ciphertext)
print (decryptedText)