from socket import *
import threading

# List to keep track of connected clients
clients = []

def handle_client(client_socket):
    """
    Handles communication with a single client.

    Args:
        client_socket (socket): The connected client socket.
    """
    # Add the new client to the list
    clients.append(client_socket)
    
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(2048).decode()
            
            # If no message is received, the client has likely disconnected
            if not message:
                break

            # Print the received message (for demonstration)
            print(f"Received: {message}") 

            # Send the message to all connected clients
            for client in clients:
                if client != client_socket:  # Don't send back to the sender
                    try:
                        response = f"CLIENT: {message}"
                        client.send(response.encode())
                    except:
                        # Remove client if there's an error sending
                        clients.remove(client) 

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    # Remove the client from the list when done
    clients.remove(client_socket)
    client_socket.close()


# Set up the server socket
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
server_socket.bind(('', server_port)) # Bind to all available interfaces on the specified port
server_socket.listen(5) # Allow up to 5 pending connections

print(f"Server is ready to receive")

while True:
    # Accept a new client connection
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")

    # Create a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()