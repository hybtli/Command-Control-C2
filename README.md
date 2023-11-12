# AKM-Python-Project

C2 Command Server and Agent

Description
This project implements a Command and Control (C2) server and agent in Python. The server allows the user to control a connected agent by sending commands such as downloading/uploading files and executing PowerShell commands.

Server
The server script (`server.py`) listens for incoming connections from agents and provides a menu-driven interface for interacting with connected agents.

Dependencies
- Python 3. x

Running the Server
1. Open a terminal.
2. Navigate to the directory containing `server.py`.
3. Run the server script:

    ```bash
    python server.py
    ```

4. The server will listen for incoming connections on IP address `0.0.0.0` and port `1234`.

Usage
- Upon connection, the server will prompt for an Agent ID, and then present a menu with options:
- `1`: Download File
- `2`: Access PowerShell
- `3`: Upload File  
- `4`: View Online Agents
- `5`: View Agent Activities
- `exit`: Exit

- For option `1`, enter the file path on the client to download.

- For option `2`, enter PowerShell commands to execute on the client.

- For option `3`, for uploading files.

- For options `4` and `5`, view online agents and agent activities, respectively.

- `exit`: Terminate the connection.

Agent
The agent script (`agent.py`) connects to the server, sends its Agent ID, and executes commands received from the server.

Dependencies
- Python 3. x

Running the Agent
1. Open a terminal.
2. Navigate to the directory containing `agent.py`.
3. Update the server IP address in the script.
4. Run the agent script:

    ```bash
    python agent.py
    ```

5. The agent will connect to the specified server IP address (`YOUR_IP_ADDRESS`) and port (`1234`).
You need to customize your server IP.

Usage
- The agent will execute commands received from the server.

Group Members and Roles
 - Nurbala : Software Engineer
 - Mirmusa:  Software Developer
 - Ogtay : Project Manager
 - Murad:  Project Manager
## Additional Remarks
- The upload feature in the server script is not implemented and can be added based on project requirements.
- Ensure that both the server and agent have the necessary permissions to perform file operations and execute commands.

Troubleshooting
- If connection issues arise, check firewall settings and ensure that the server IP address is correctly configured in the agent script.

## Notes
We could not fix the encryption method and it is affecting our project. Please consider these during evaluation.
