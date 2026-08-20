from socket import *
import random

SIMULATE_ATTACK = True  # Set to True to simulate wrong secret
SERVER_NAME = "127.0.0.1"
SERVER_PORT = 1300
BUFFER_SIZE = 65000


# Old trial division (slow for large numbers):
# def is_prime(n):
#     if n <= 1:
#         return False
#     for i in range(2, int(n**0.5) + 1):
#         if n % i == 0:
#             return False
#     return True

def is_prime(n, k=20):
    """Check if a number is prime using Miller-Rabin primality test.

    Args:
        n: number to test
        k: number of rounds (higher = more accurate)

    Returns:
        True if probably prime, False if definitely composite
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = mod_exp(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_prime(bits=8):
    """Generate a random prime number with the given bit length."""
    prime = random.getrandbits(bits)
    while not is_prime(prime):
        prime = random.getrandbits(bits)
    return prime


def find_generator(p):
    """Find a primitive root (generator) modulo p."""
    return random.randint(2, p - 1)


def mod_exp(base, exponent, modulus):
    """Compute (base^exponent) mod modulus efficiently."""
    return (base**exponent) % modulus


def xor_encrypt(message, key):
    """Encrypt a message by XORing each byte with the key."""
    encrypted = bytes([b ^ (key % 256) for b in message.encode("utf-8")])
    return encrypted


def xor_decrypt(encrypted, key):
    """Decrypt a message by XORing each byte with the key."""
    decrypted = bytes([b ^ (key % 256) for b in encrypted])
    return decrypted.decode("utf-8")


def diffie_hellman_client(p, g):
    """Perform Diffie-Hellman key exchange on client side.

    Args:
        p: prime modulus received from server
        g: generator received from server

    Returns:
        (B, private_key_b): public value and private key
    """
    print("  Generating private key b...")
    private_key_b = random.randrange(p)

    print("  Computing B = g^b mod p...")
    B = mod_exp(g, private_key_b, p)

    return B, private_key_b


def connect_to_server(server_name, server_port):
    """Create a socket and connect to the server."""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    return client_socket


def receive_message(client_socket):
    """Receive data from the server."""
    data = client_socket.recv(BUFFER_SIZE)
    return str(data, "utf-8")


def send_message(client_socket, message):
    """Send a string message to the server."""
    client_socket.send(bytes(message, "utf-8"))


def send_message_bytes(client_socket, data):
    """Send raw bytes to the server."""
    client_socket.send(data)


def main():
    client_socket = connect_to_server(SERVER_NAME, SERVER_PORT)
    print()
    print("=" * 50)
    print("DIFFIE-HELLMAN KEY EXCHANGE")
    print("=" * 50)
    print()

    # Step 1: Receive public values (p, g) from server
    print("STEP 1: Receive public parameters from server")
    print("-" * 50)
    p = int(receive_message(client_socket))
    g = int(receive_message(client_socket))
    print(f"  Prime modulus (p) = {p}")
    print(f"  Generator     (g) = {g}")
    print()

    # Step 2: Compute client's public value B and shared secret
    print("STEP 2: Compute client's public value B")
    print("-" * 50)
    B, private_key_b = diffie_hellman_client(p, g)
    print(f"  Client's private key (b) = [hidden]")
    print(f"  B = g^b mod p = {g}^{private_key_b} mod {p} = {B}")
    print(f"  Sending B to server...")
    send_message(client_socket, str(B))
    print()

    # Step 3: Receive A from server and compute shared secret
    print("STEP 3: Receive server's public value A")
    print("-" * 50)
    A = int(receive_message(client_socket))
    print(f"  Received A = {A}")
    print(f"  (Server computed A = g^a mod p, where a is server's private key)")
    print()

    print("STEP 4: Compute shared secret")
    print("-" * 50)
    shared_secret = mod_exp(A, private_key_b, p)
    print(f"  shared_secret = A^b mod p = {A}^{private_key_b} mod {p}")
    print(f"  shared_secret = {shared_secret}")
    print()

    print("=" * 50)
    print("SECURE CHANNEL ESTABLISHED!")
    print("=" * 50)
    print(f"  Both sides now share the same secret: {shared_secret}")
    print(f"  (Server computed it as B^a mod p)")
    print(f"  An eavesdropper sees p={p}, g={g}, A={A}, B={B}")
    print(f"  but CANNOT compute the shared secret without a or b!")
    print()

    print("=" * 50)
    print("STEP 5: Encrypted communication")
    print("=" * 50)

    sentence = input("  Input message: ")

    # Encrypt and send
    if SIMULATE_ATTACK:
        attack_key = shared_secret + 50
        print(f"  [ATTACK] Using wrong key: {attack_key} (real: {shared_secret})")
        encrypted = xor_encrypt(sentence, attack_key)
    else:
        encrypted = xor_encrypt(sentence, shared_secret)
    print(f"  Sending encrypted: {encrypted.hex()}")
    send_message_bytes(client_socket, encrypted)

    # Receive and decrypt
    encrypted_response = client_socket.recv(BUFFER_SIZE)
    print(f"  Received encrypted: {encrypted_response.hex()}")
    if SIMULATE_ATTACK:
        response = xor_decrypt(encrypted_response, attack_key)
    else:
        response = xor_decrypt(encrypted_response, shared_secret)
    print(f"  Decrypted: {response}")

    client_socket.close()
    print()
    print("Connection closed.")


if __name__ == "__main__":
    main()
