import datetime
import sys

def generate_primes():
    # Get UTC time
    time = datetime.datetime.utcnow()
    hour = time.hour
    minute = time.hour + 1

    prime_list = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107]
    list_len = len(prime_list)

    # Implement a sort of diffie-hellman
    # Get a and b
    p = prime_list[hour]
    g = prime_list[minute % list_len]

    return p,g

def generate_secret(node):
    # Get UTC time
    time = datetime.datetime.utcnow()
    hour = time.hour
    minute = time.hour + 1

    prime_list = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107]
    list_len = len(prime_list)

    # Generate secrets for each node
    a = prime_list[(hour+node) % list_len]
    b = prime_list[(minute+node) % list_len]

    p,g = generate_primes()

    # g^a % p
    temp_secret1 = pow(g,a) % p
    # g^b % p
    temp_secret2 = pow(g,b) % p

    secret1 = pow(temp_secret2,a) % p
    secret2 = pow(temp_secret1,a) % p

    return secret1, secret2
