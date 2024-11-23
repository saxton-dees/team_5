from socket import *
import threading

def handle_client(client_socket):
    """
    Handles communication with a single client.

    Args:
        client_socket (socket): The connected client socket.
    """
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(2048).decode()
            
            # If no message is received, the client has likely disconnected
            if not message:
                break

            # Print the received message (for demonstration)
            print(f"Received: {message}") 

            # Send a response back to the client
            response = f"SERVER: {message}"  # Simple echo for now
            client_socket.send(response.encode())

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    # Close the client socket when done
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
