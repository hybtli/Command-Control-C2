import socket
import threading

from Dashboard import handle_agent


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 1234))
    server.listen(5)

    print("Server is listening...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")

        agent_handler = threading.Thread(target=handle_agent, args=(client_socket, client_address))
        agent_handler.start()
        server.close()
        break


if __name__ == "__main__":
    main()
