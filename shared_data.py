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


help_msg = f"""
{"=" * 80}
{"/" * 80}
{"=" * 80}

/connect <server-name> [port#] - Connect to named server (port# optional)
/nick <nickname> - Pick a nickname (should be unique among active users)
/join <channel> - Join a channel
/leave [<channel>] - Leave the current (or named) channel
/list - List channels and number of users
/msg <nickname> <message> - Send a private message to a user
/help - Print out this help message

{"=" * 80}
{"/" * 80}
{"=" * 80}
"""