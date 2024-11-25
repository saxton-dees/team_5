from socket import *
import threading

class Client:
    def __init__(self, socket):
        self.socket = socket
        self.channel = None 
        self.nickname = self.socket.getpeername()

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
            try:
                client.socket.send(message.encode())
            except Exception as e:
                print(f"Error broadcasting message: {e}")


def handle_client(client_socket):
    """Handles communication with a single client."""
    client = Client(client_socket)
    clients.append(client)

    while True:
        try:
            message = client.socket.recv(2048).decode()
            if not message:
                break

            if message.startswith("/join"):
                channel_name = message.split("/join")[1].strip()
                channel = next((c for c in channels if c.name == channel_name), None)
                if not channel:
                    channel = Channel(channel_name)
                    channels.append(channel)
                    client.socket.send(f'Channel {channel_name} has been created.\n'.encode())
                channel.clients.append(client)
                client.channel = channel

                join_message = f"You have joined channel: {channel.name}"
                client.socket.send(join_message.encode())
                broadcast(client.socket, f"SERVER: {client.nickname} has joined the channel.", channel)

            elif message.startswith("/leave"):
                if client.channel:
                    channel_name = client.channel.name
                    leave_message = f"You are leaving channel: {channel_name}"
                    client.socket.send(leave_message.encode())
                    broadcast(client.socket, f"SERVER: {client.nickname} has left the channel.", client.channel)
                    client.channel.clients.remove(client)
                    client.channel = None

            elif message.startswith("/nick"):
                new_nickname = message.split("/nick")[1].strip()
                if new_nickname:
                    old_nickname = client.nickname
                    client.nickname = new_nickname
                    if client.channel:
                        broadcast(client.socket, f"SERVER: {old_nickname} is now known as {client.nickname}.", client.channel)

            elif message.startswith("/list"):
                if channels:
                    channel_list = "Channels:\n" + "\n".join([f"{c.name} ({len(c.clients)} users)" for c in channels])
                    client.socket.send(channel_list.encode())
                else:
                    client.socket.send("No channels available.".encode())

            elif message.startswith("/msg"):
                try:
                    parts = message.split()
                    target_nickname = parts[1]
                    private_message = " ".join(parts[2:])
                    target_client = next((c for c in clients if c.nickname == target_nickname), None)
                    if target_client:
                        target_client.socket.send(f"PRIVATE MESSAGE from {client.nickname}: {private_message}".encode())
                        client.socket.send(f"PRIVATE MESSAGE to {target_nickname}: {private_message}".encode())
                    else:
                        client.socket.send(f"SERVER: User {target_nickname} not found.".encode())
                except IndexError:
                    client.socket.send("Invalid /msg command format. Usage: /msg <nickname> <message>".encode())

            elif message.startswith("/quit"):
                client.socket.send("Goodbye!".encode())
                break 

            elif message.startswith("/help"):
                help_msg = "/connect <server-name> [port#] - Connect to named server (port# optional)"
                help_msg += "\n/nick <nickname> - Pick a nickname (should be unique among active users)"
                help_msg += "\n/join <channel> - Join a channel"
                help_msg += "\n/leave [<channel>] - Leave the current (or named) channel"
                help_msg += "\n/list - List channels and number of users"
                help_msg += "\n/msg <nickname> <message> - Send a private message to a user"
                help_msg += "\n/help - Print out this help message"
                client.socket.send(help_msg.encode())
            else:
                if client.channel:
                    response = f"{client.nickname}: {message}"
                    broadcast(client.socket, response, client.channel)
                else:
                    client.socket.send("You are not in a channel. Use /join <channel_name> to join one.".encode())

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