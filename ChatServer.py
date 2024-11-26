import argparse
import json
import threading
import time
from socket import *
from colorama import Fore, Style, init

from CommandHandlers import *  # Import command handlers
from SharedData import *  # Import shared data (clients, channels, etc.)

init(autoreset=True)  # Initialize colorama for automatic style resets

last_activity_time = time.time()  # Initialize with the current time

IDLE_TIMEOUT = 3 * 60  # 3 minutes in seconds

def handle_client(client_socket):
    """Handles communication with a single client."""
    global last_activity_time  # Use the global activity tracker

    # Create a Client object and add it to the clients list
    client = Client(client_socket)
    clients.append(client)

    while True:  # Main loop for handling client communication
        try:
            data = client_socket.recv(2048).decode()  # Receive data from the client
            if not data:  # If no data is received, client has disconnected
                break

            message = json.loads(data)  # Deserialize the JSON message

            last_activity_time = time.time()

            # Handle different message types
            if message["type"] == "join":
                handle_join(client, message, channels)
            elif message["type"] == "leave":
                handle_leave(client, message)
            elif message["type"] == "nick":
                handle_nick(client, message)
            elif message["type"] == "list":
                handle_list(client, message)
            elif message["type"] == "msg":
                handle_msg(client, message)
            elif message["type"] == "quit":
                handle_quit(client, message)
                break  # Exit the loop if the client quits
            elif message["type"] == "help":
                handle_help(client, message)
            else:  # If the message type is not recognized
                if client.channel:  # If the client is in a channel
                    # Construct a chat message and broadcast it to the channel
                    response = {
                        "type": "chat_message",
                        "sender": client.nickname,
                        "message": message["message"],
                    }
                    broadcast(client_socket, response, client.channel)
                else:  # If the client is not in a channel
                    # Send a server message informing the client to join a channel
                    send_server_message(
                        client,
                        Fore.RED
                        + "You are not in a channel. Use /join <channel_name> to join one."
                        + Style.RESET_ALL,
                    )

        except Exception as e:  # Handle any exceptions during client communication
            print(Fore.RED + f"Error handling client: {e}" + Style.RESET_ALL)
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

def idle_timeout_checker():
    """Checks for idle timeout and shuts down the server if unused."""
    global last_activity_time

    while True:
        time_since_last_activity = time.time() - last_activity_time
        if time_since_last_activity > IDLE_TIMEOUT:
            print(Fore.RED + "Server has been idle for over 3 minutes. Shutting down..." + Style.RESET_ALL)
            shutdown_server()
            break
        time.sleep(10)  # Check every 10 seconds


def shutdown_server():
    """Shuts down the server gracefully."""
    for client in clients:
        client.socket.close()
    print(Fore.RED + "Server shutting down..." + Style.RESET_ALL)
    exit(0)


if __name__ == "__main__":

    # setting up argument parsing
    parser = argparse.ArgumentParser(
        prog="ChatServer",
        description="Basic chat server supporting multiple clients over the Internet",
    )
    parser.add_argument(
        "-p", type=int, choices=range(12000, 12050), default=12000, help="port number (between 12000 and 12049)"
    )
    parser.add_argument("-d", type=int, choices=[0, 1], default=0, help="debug level (0 or 1)")
    args = parser.parse_args()
    # parser.print_help()

    # storing values
    server_port = args.p  # Define the server port
    debug_level = args.d

    # Server setup
    server_socket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
    server_socket.bind(("", server_port))  # Bind the socket to the port
    server_socket.listen(5)  # Listen for incoming connections

    print(Fore.GREEN + f"Server is ready to receive" + Style.RESET_ALL)

    idle_thread = threading.Thread(target=idle_timeout_checker, daemon=True)
    idle_thread.start()

    while True:  # Main loop for accepting client connections
        try:
            client_socket, addr = server_socket.accept()  # Accept a connection from a client
            print(Fore.CYAN + f"Accepted connection from {addr}" + Style.RESET_ALL)
            client_socket.send(
                json.dumps(help_msg).encode()
            )  # Send the help message to the client
            # Create a new thread to handle the client communication
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()  # Start the thread
        except KeyboardInterrupt:
            print(Fore.RED + "\nServer shutting down gracefully..." + Style.RESET_ALL)
            shutdown_server()
            break