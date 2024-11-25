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


def handle_join(client, message):
    """Handles the /join command."""
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


def handle_leave(client, message):
    """Handles the /leave command."""
    if client.channel:
        channel_name = client.channel.name
        leave_message = f"You are leaving channel: {channel_name}"
        client.socket.send(leave_message.encode())
        broadcast(client.socket, f"SERVER: {client.nickname} has left the channel.", client.channel)
        client.channel.clients.remove(client)
        client.channel = None


def handle_nick(client, message):
    """Handles the /nick command."""
    new_nickname = message.split("/nick")[1].strip()
    if new_nickname:
        old_nickname = client.nickname
        client.nickname = new_nickname
        if client.channel:
            broadcast(client.socket, f"SERVER: {old_nickname} is now known as {client.nickname}.", client.channel)


def handle_list(client, message):
    """Handles the /list command."""
    if channels:
        channel_list = "Channels:\n" + "\n".join([f"{c.name} ({len(c.clients)} users)" for c in channels])
        client.socket.send(channel_list.encode())
    else:
        client.socket.send("No channels available.".encode())


def handle_msg(client, message):
    """Handles the /msg command."""
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


def handle_quit(client, message):
    """Handles the /quit command."""
    client.socket.send("Goodbye!".encode())
    # This will cause the loop in handle_client to break


def handle_help(client, message):
    """Handles the /help command."""
    help_msg = "/connect <server-name> [port#] - Connect to named server (port# optional)"
    help_msg += "\n/nick <nickname> - Pick a nickname (should be unique among active users)"
    help_msg += "\n/join <channel> - Join a channel"
    help_msg += "\n/leave [<channel>] - Leave the current (or named) channel"
    help_msg += "\n/list - List channels and number of users"
    help_msg += "\n/msg <nickname> <message> - Send a private message to a user"
    help_msg += "\n/help - Print out this help message"
    client.socket.send(help_msg.encode())


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
                handle_join(client, message)

            elif message.startswith("/leave"):
                handle_leave(client, message)

            elif message.startswith("/nick"):
                handle_nick(client, message)

            elif message.startswith("/list"):
                handle_list(client, message)

            elif message.startswith("/msg"):
                handle_msg(client, message)

            elif message.startswith("/quit"):
                handle_quit(client, message)
                break  # Break the loop after handling /quit

            elif message.startswith("/help"):
                handle_help(client, message)

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