from socket import *

SERVER_PORT = 1300
BUFFER_SIZE = 65000
SHIFT = 60

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

def create_server_socket(port):
    """Create, bind and start listening on a TCP server socket."""
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)
    print("TCP Server running on port", port)
    return server_socket


def receive_message(connection_socket):
    """Receive data from the client connection."""
    data = connection_socket.recv(BUFFER_SIZE)
    return str(data, "utf-8")


def process_message(message):
    """Process the received message. Currently converts to uppercase."""
    return message.upper()


def send_message(connection_socket, message):
    """Send a string message back to the client."""
    connection_socket.send(bytes(message, "utf-8"))


def main():
    server_socket = create_server_socket(SERVER_PORT)
    connection_socket, addr = server_socket.accept()
    print("Connection from", addr)

    received = receive_message(connection_socket)
    print("Received From Client:", received)
    
    received_decrypted = caesar_decrypt(received, SHIFT)
    print("Received From Client decrypted:", received_decrypted)
    
    processed = process_message(received_decrypted)
    print("Processed:", processed)

    encrypt_processed = caesar_encrypt(processed, SHIFT)
    send_message(connection_socket, encrypt_processed)
    print("Sent back to Client encrypted:", encrypt_processed)

    connection_socket.close()


if __name__ == "__main__":
    main()
