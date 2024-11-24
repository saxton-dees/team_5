from socket import *
import threading

class Client:
    def __init__(self, socket):
        self.socket = socket
        self.channel = None 

class Channel:
    def __init__(self, name):
        self.name = name
        self.clients = []


channels = []  
clients = []


def broadcast(client_socket, message, channel):
    """Broadcasts a message to all clients in a channel except the sender."""
    for client in channel.clients:
        if client.socket != client_socket:
                client.socket.send(message.encode())


def handle_client(client_socket):
    """Handles communication with a single client."""
    client = Client(client_socket)
    clients.append(client)

    while True:
        try:
            message = client_socket.recv(2048).decode()
            if not message:
                break

            if message.startswith("/join"):
                channel_name = message.split("/join")[1].strip()
                channel = next((c for c in channels if c.name == channel_name), None)
                if not channel:
                    channel = Channel(channel_name)
                    channels.append(channel)
                    client_socket.send(f'Channel {channel_name} has been created.\n'.encode())
                channel.clients.append(client)
                client.channel = channel

                join_message = f"You have joined channel: {channel.name}"
                client_socket.send(join_message.encode())
                broadcast(client_socket, f"SERVER: {client_socket.getpeername()} has joined the channel.", channel)

            elif message.startswith("/leave"):
                if client.channel:
                    channel_name = client.channel.name
                    leave_message = f"You are leaving channel: {channel_name}"
                    client_socket.send(leave_message.encode())
                    broadcast(client_socket, f"SERVER: {client_socket.getpeername()} has left the channel.", client.channel)
                    client.channel.clients.remove(client)
                    client.channel = None

            else:
                if client.channel:
                    response = f"CLIENT {client_socket.getpeername()}: {message}"
                    broadcast(client_socket, response, client.channel)
                else:
                    client_socket.send("You are not in a channel. Use /join <channel_name> to join one.".encode())

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    remove_client(client_socket)


def remove_client(client_socket):
    """Removes a client from the clients list and any channel they were in."""
    for client in clients:
        if client.socket == client_socket:
            if client.channel:
                client.channel.clients.remove(client)
            clients.remove(client)
            break
    client_socket.close()


server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(5)

print(f"Server is ready to receive")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
