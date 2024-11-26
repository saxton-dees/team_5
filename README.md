# Chat Server and Client

## Team Members

*   [Saxton Dees, <id>]
*   [Upama Thapa Magar, <114264958>]

## Demo Video

[Link to your YouTube/Panopto video]

## Overview

This project implements a basic chat server and client using Python. The server supports multiple clients connecting over the internet, allowing them to join channels, send private messages, and change their nicknames.

## Features

* **Multiple Clients:** Handles concurrent connections from multiple users.
* **Channels:** Users can join and leave channels to communicate in groups.
* **Private Messaging:**  Users can send private messages to other users.
* **Nickname Changes:** Users can change their nicknames.
* **Command-line Interface:** Simple and easy-to-use command-line interface for both server and client.

## File/Folder Manifest

*   `ChatServer.py`: The chat server implementation.
*   `ChatClient.py`: The chat client implementation.
*   `SharedData.py`: Contains shared data structures (clients, channels) and functions used by both server and client.
*   `CommandHandlers.py`: Contains functions to handle different client commands (join, leave, nick, etc.).
*   `requirements.txt`: Lists the project's Python dependencies.

## Building and Running

### Prerequisites

* Python 3.x

### Server

1.  Clone the repository: `git clone <repository_url>`
2.  Navigate to the project directory: `cd chat-server-client`
3.  Create and activate a virtual environment (recommended):
    ```bash
    python3 -m venv venv
    . venv/bin/activate
    ```
4.  Install dependencies: `pip install -r requirements.txt`
5.  Run the server: 
    ```bash
    python ChatServer.py -p <port-number> -d <debug-level> 
    ```
    (e.g., `python ChatServer.py -p 12000 -d 0`)

### Client

1.  Open a **new** terminal window.
2.  Activate the same virtual environment: `source venv/bin/activate`
3.  Run the client: `python ChatClient.py`
4.  You can run multiple clients in separate terminal windows to simulate multiple users.

##  Development

This project uses `black` and `isort` to maintain code style and consistency.

*   **black:**  Code formatter.
*   **isort:**  Sorts imports alphabetically and separates them into sections.

To format your code, run:

```bash
black .
isort .