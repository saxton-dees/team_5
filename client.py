from socket import *

# Set up the client socket 
server_port = 12000
client_socket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
client_socket.connect(('', server_port))  # Connect to the server

while True:
    # Get message from the user
    message = input()

    # Send the message to the server
    client_socket.send(message.encode())

    # Receive the response from the server
    response = client_socket.recv(2048).decode()

    # Print the server's response
    print(response)