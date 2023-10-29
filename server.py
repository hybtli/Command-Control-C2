import socket

SERVER_HOST = '0.0.0.0'  # Accept connections from any source
SERVER_PORT = 12345  # Server port


# Function to start the server
def start_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        return s
    except socket.error as e:
        print(f"Error starting server: {e}")
        return None


# Function to receive a file from the client
def receive_file(client_socket, file_path):
    try:
        with open(file_path, 'wb') as f:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                f.write(data)
    except IOError as e:
        print(f"Error receiving file: {e}")


if __name__ == '__main__':
    # Start the server
    server_socket = start_server()
    if server_socket:
        # Accept client connection
        client_socket, client_address = server_socket.accept()
        print(f"[*] Connection from {client_address[0]}:{client_address[1]}")

        # Define the path to save the received file
        file_path = 'received_file'  # Specify the path to save the received file
        # Receive the file from the client
        receive_file(client_socket, file_path)

        # Close the client socket connection
        client_socket.close()
