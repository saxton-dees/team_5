# Chat Server and Client

## Team Members

*   [Saxton Dees, <id>]

## Demo Video

[Link to your YouTube/Panopto video]

## File/Folder Manifest

*   `ChatServer.py`: The chat server implementation.
*   `ChatClient.py`: The chat client implementation.
*   `SharedData.py`: Contains shared data structures and functions used by both server and client.
*   `CommandHandlers.py`: Contains functions to handle different client commands.

## Building and Running

### Server

1.  Make sure you have Python 3 installed.
2.  Save all the files in the same directory.
3.  Open a terminal and navigate to the directory where you saved the files.
4.  Run the server using the command `
    ```
    python ChatServer.py -p <port-number> -d <debug-level>
    ```

### Client

1.  Open a **new** terminal window.
2.  Navigate to the same directory where you saved the files.
3.  Run the client using the command=
    ```
    python ChatClient.py
    ```
4.  You can run multiple clients in separate terminal windows to simulate multiple users.
