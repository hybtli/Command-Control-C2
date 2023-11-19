import os

'''
def upload_file(client_socket, file_path, agent_id):
    try:
        send_file(client_socket, file_path)
        # Send a signal to the client indicating that the file upload is complete
        client_socket.send("File upload complete".encode('utf-8'))
    except Exception as e:
        print(f"Error uploading file: {e}")
'''


def receive_file_from_client(client_socket, file_path):
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


'''
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
'''
