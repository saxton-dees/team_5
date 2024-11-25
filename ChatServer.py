import json
from socket import *
import threading
from SharedData import *  # Import shared data (clients, channels, etc.)
from CommandHandlers import *  # Import command handlers

def handle_client(client_socket):
    """Handles communication with a single client."""

    # Create a Client object and add it to the clients list
    client = Client(client_socket)  
    clients.append(client)

    while True:  # Main loop for handling client communication
        try:
            data = client_socket.recv(2048).decode()  # Receive data from the client
            if not data:  # If no data is received, client has disconnected
                break

            message = json.loads(data)  # Deserialize the JSON message

            # Handle different message types
            if message['type'] == 'join':  
                handle_join(client, message, channels)
            elif message['type'] == 'leave':
                handle_leave(client, message)
            elif message['type'] == 'nick':
                handle_nick(client, message)
            elif message['type'] == 'list':
                handle_list(client, message)
            elif message['type'] == 'msg':
                handle_msg(client, message)
            elif message['type'] == 'quit':
                handle_quit(client, message)
                break  # Exit the loop if the client quits
            elif message['type'] == 'help':
                handle_help(client, message)
            else:  # If the message type is not recognized
                if client.channel:  # If the client is in a channel
                    # Construct a chat message and broadcast it to the channel
                    response = {'type': 'chat_message', 'sender': client.nickname, 'message': message['message']}  
                    broadcast(client_socket, response, client.channel)
                else:  # If the client is not in a channel
                    # Send a server message informing the client to join a channel
                    send_server_message(client, "You are not in a channel. Use /join <channel_name> to join one.") 

        except Exception as e:  # Handle any exceptions during client communication
            print(f"Error handling client: {e}")
            break

    remove_client(client_socket)  # Remove the client when the connection is closed


def remove_client(client_socket):
    """Removes a client from the clients list and any channel they were in."""
    for client in clients:
        if client.socket == client_socket:
            if client.channel:
                client.channel.clients.remove(client)
            clients.remove(client)
            break
    client_socket.close()


# Server setup
server_port = 12000  # Define the server port
server_socket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
server_socket.bind(('', server_port))  # Bind the socket to the port
server_socket.listen(5)  # Listen for incoming connections

print(f"Server is ready to receive")

while True:  # Main loop for accepting client connections
    client_socket, addr = server_socket.accept()  # Accept a connection from a client
    print(f"Accepted connection from {addr}")
    client_socket.send(json.dumps(help_msg).encode())  # Send the help message to the client
    # Create a new thread to handle the client communication
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))  
    client_handler.start()  # Start the thread