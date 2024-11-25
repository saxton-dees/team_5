class Client:
    def __init__(self, socket):
        self.socket = socket
        self.channel = None 
        self.nickname = self.socket.getpeername()


class Channel:
    def __init__(self, name):
        self.name = name
        self.clients = []


def broadcast(client_socket, message, channel):
    """Broadcasts a message to all clients in a channel except the sender."""
    for client in channel.clients:
        if client.socket != client_socket:
            try:
                client.socket.send(message.encode())
            except Exception as e:
                print(f"Error broadcasting message: {e}")


channels = []
clients = []


help_msg = "=" * 80
help_msg += "\n"
help_msg += "\/" * 40
help_msg += "\n"
help_msg += "=" * 80
help_msg += "\n/connect <server-name> [port#] - Connect to named server (port# optional)"
help_msg += "\n/nick <nickname> - Pick a nickname (should be unique among active users)"
help_msg += "\n/join <channel> - Join a channel"
help_msg += "\n/leave [<channel>] - Leave the current (or named) channel"
help_msg += "\n/list - List channels and number of users"
help_msg += "\n/msg <nickname> <message> - Send a private message to a user"
help_msg += "\n/help - Print out this help message"
help_msg += "\n"
help_msg += "=" * 80
help_msg += "\n"
help_msg += "\/" * 40
help_msg += "\n"
help_msg += "=" * 80