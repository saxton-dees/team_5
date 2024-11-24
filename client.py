from socket import *
import threading

# Set up the client socket
server_port = 12000
client_socket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
client_socket.connect(('', server_port))  # Connect to the server

def receive_messages():
    while True:
        try:
            response = client_socket.recv(2048).decode()
            print(response)
        except:
            break

# Create and start the receive thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input()
    client_socket.send(message.encode())