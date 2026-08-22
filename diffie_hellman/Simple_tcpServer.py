from socket import *
import random

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

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform k rounds of testing
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
    print(f"  Finding a {bits}-bit prime number...")
    attempts = 0
    while True:
        attempts += 1
        prime = random.getrandbits(bits)
        if prime % 2 == 0:
            prime += 1
        if is_prime(prime):
            print(f"  Found prime after {attempts} attempts")
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


def caesar_encrypt(plain_text, shift):
    """Encrypt plain_text using Caesar cipher with the given shift."""
    # TODO: implement Caesar cipher encryption
    # Should shift each letter by 'shift' positions, wrapping around Z->A
    
    output_string = ""
    for letter in plain_text:
        value = ord(letter)
        new_value = value + shift
        output_string += chr(new_value)
    
    return output_string


def caesar_decrypt(cipher_text, shift):
    """Decrypt cipher_text using Caesar cipher with the given shift."""
    # TODO: implement Caesar cipher decryption
    # Should reverse the shift applied during encryption
    
    output_string = ""
    for letter in cipher_text:
        value = ord(letter)
        new_value = value - shift
        output_string += chr(new_value)
    
    return output_string


def diffie_hellman_server(public_values):
    """Perform Diffie-Hellman key exchange on server side.

    Args:
        public_values: dict with 'p', 'g', 'B' from client

    Returns:
        (A, shared_secret): server's public value and the computed shared secret
    """
    p = public_values.get("p")
    g = public_values.get("g")
    B = public_values.get("B")

    print("  Generating private key a...")
    private_key_a = random.randrange(p)

    print("  Computing A = g^a mod p...")
    A = mod_exp(g, private_key_a, p)

    print("  Computing shared_secret = B^a mod p...")
    shared_secret = mod_exp(B, private_key_a, p)

    return A, shared_secret


def create_server_socket(port):
    """Create, bind and start listening on a TCP server socket."""
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(5)
    print("TCP Server running on port", port)
    return server_socket


def receive_message(connection_socket):
    """Receive data from the client connection."""
    data = connection_socket.recv(BUFFER_SIZE)
    return str(data, "utf-8")


def send_message(connection_socket, message):
    """Send a string message to the client."""
    connection_socket.send(bytes(message, "utf-8"))


def main():
    server_socket = create_server_socket(SERVER_PORT)
    connection_socket, addr = server_socket.accept()
    print("Connection from", addr)
    print()

    # Step 1: Server generates and sends public values (p, g)
    print("=" * 50)
    print("STEP 1: Server generates public parameters")
    print("=" * 50)
    p = generate_prime()
    g = find_generator(p)
    print(f"  Prime modulus (p)    = {p}")
    print(f"  Generator    (g)     = {g}")
    print(f"  Sending p and g to client...")
    send_message(connection_socket, str(p))
    send_message(connection_socket, str(g))
    print()

    # Step 2: Receive B from client
    print("=" * 50)
    print("STEP 2: Receive client's public value B")
    print("=" * 50)
    B = int(receive_message(connection_socket))
    print(f"  Received B = {B}")
    print(f"  (Client computed B = g^b mod p, where b is client's private key)")
    print()

    # Step 3: Compute server's public value A and shared secret
    print("=" * 50)
    print("STEP 3: Server computes A and shared secret")
    print("=" * 50)
    A, shared_secret = diffie_hellman_server({"p": p, "g": g, "B": B})
    print(f"  Server's private key (a) = [hidden]")
    print(f"  Server's public value (A) = g^a mod p = {A}")
    print(f"  Sending A to client...")
    send_message(connection_socket, str(A))
    print()
    print(f"  Computing shared secret = B^a mod p")
    print(f"  Shared secret = {shared_secret}")
    print()

    print("=" * 50)
    print("STEP 4: Secure channel established!")
    print("=" * 50)
    print(f"  Both sides now share the same secret: {shared_secret}")
    print(f"  (Client computed it as A^b mod p)")
    print(f"  An eavesdropper sees p, g, A, B but cannot compute the secret!")
    print()

    print("=" * 50)
    print("STEP 5: Encrypted communication")
    print("=" * 50)

    # Receive encrypted message from client
    received_data = connection_socket.recv(BUFFER_SIZE)
    encrypted_received_data = str(received_data, "utf-8")
    print(f"  Received encrypted: {encrypted_received_data}")
    try:
        message = caesar_decrypt(encrypted_received_data, shared_secret)
        print(f"  Decrypted: {message}")
    except UnicodeDecodeError:
        print("  Decryption failed: message was not encrypted with the shared secret!")
        connection_socket.close()
        return

    # Process and send back encrypted response
    response = message.upper()
    encrypted_response = caesar_encrypt(response, shared_secret)
    print(f"  Sending encrypted: {encrypted_response}")
    connection_socket.send(bytes(encrypted_response,"utf-8"))

    connection_socket.close()
    print()
    print("Connection closed.")


if __name__ == "__main__":
    main()
