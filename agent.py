import socket
import os

SERVER_HOST = 'your_server_ip'  # Server IP address
SERVER_PORT = 12345  # Server port

# Function to establish a connection to the server
def connect_to_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_HOST, SERVER_PORT))
        return s
    except socket.error as e:
        print(f"Error connecting to server: {e}")
        return None

# Function to send data to the server
def send_data(s, data):
    try:
        s.send(data)
    except socket.error as e:
        print(f"Error sending data: {e}")

# Function to send a file to the server
def send_file(s, file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            s.send(data)
    except IOError as e:
        print(f"Error sending file: {e}")

if __name__ == '__main__':
    # Connect to the server
    server_socket = connect_to_server()
    if server_socket:
        current_dir = os.getcwd()
        # Send the current directory to the server
        send_data(server_socket, f"Agent connected from {current_dir}")

        # Define the path of the file to be sent
        file_path = 'path_to_your_file'  # Replace with the actual file path
        # Send the file to the server
        send_file(server_socket, file_path)

        # Close the socket connection
        server_socket.close()
