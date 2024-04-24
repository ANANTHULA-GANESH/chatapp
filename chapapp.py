import socket
import threading

def handle_client(client_socket, client_address, clients):
    """
    Handle a client connection.
    
    Args:
    client_socket (socket.socket): Client socket object.
    client_address (tuple): Client address (IP, port).
    clients (list): List of connected clients.
    """
    print(f"Accepted connection from {client_address}")
    
    # Add client to the list
    clients.append(client_socket)
    
    try:
        while True:
            # Receive message from the client
            message = client_socket.recv(1024).decode("utf-8")
            
            if not message:
                break
            
            print(f"Received message from {client_address}: {message}")
            
            # Broadcast the message to all connected clients except the sender
            for client in clients:
                if client != client_socket:
                    client.send(message.encode("utf-8"))
                    
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        # Close the client socket
        client_socket.close()
        clients.remove(client_socket)
        print(f"Connection from {client_address} closed")

def receive_messages(client_socket):
    """
    Receive messages from the server.
    
    Args:
    client_socket (socket.socket): Client socket object.
    """
    try:
        while True:
            # Receive message from the server
            message = client_socket.recv(1024).decode("utf-8")
            
            if not message:
                break
            
            print(f"\nReceived message: {message}")
            
    except Exception as e:
        print(f"Error receiving message: {e}")
        client_socket.close()
        exit()

def send_messages(client_socket):
    """
    Send messages to the server.
    
    Args:
    client_socket (socket.socket): Client socket object.
    """
    try:
        while True:
            # Get user input for message
            message = input("")
            
            # Send message to the server
            client_socket.send(message.encode("utf-8"))
            
    except Exception as e:
        print(f"Error sending message: {e}")
        client_socket.close()
        exit()

def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port
    server_socket.bind(("localhost", 5555))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print("Server is listening on port 5555")
    
    # List to keep track of connected clients
    clients = []
    
    try:
        while True:
            # Accept a new connection
            client_socket, client_address = server_socket.accept()
            
            # Start a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
            client_thread.start()
            
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        # Close all client connections
        for client in clients:
            client.close()
        
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    main()
