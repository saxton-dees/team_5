from socket import *
import threading
from shared_data import *
from command_handlers import handle_join, handle_leave, handle_nick, handle_list, handle_msg, handle_quit, handle_help


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
                handle_join(client, message, channels)

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
                break

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
    client_socket.send(help_msg.encode())
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()