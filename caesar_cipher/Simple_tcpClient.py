from socket import *

SERVER_NAME = "10.1.73.10"
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


def connect_to_server(server_name, server_port):
    """Create a socket and connect to the server."""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    return client_socket


def send_message(client_socket, message):
    """Send a string message to the server."""
    client_socket.send(bytes(message, "utf-8"))


def receive_message(client_socket):
    """Receive a response from the server."""
    data = client_socket.recv(BUFFER_SIZE)
    return str(data, "utf-8")


def main():
    client_socket = connect_to_server(SERVER_NAME, SERVER_PORT)

    sentence = input("Input lowercase sentence: ")

    encrypted_sentence = caesar_encrypt(sentence, SHIFT)

    send_message(client_socket, encrypted_sentence)
    
    response = receive_message(client_socket)
    response_decrypted = caesar_decrypt(response, SHIFT)
    print("Received from Server:", response_decrypted)

    client_socket.close()


if __name__ == "__main__":
    main()
