from shared_data import *

def handle_join(client, message, channels):
    """Handles the /join command."""
    channel_name = message.split("/join")[1].strip()
    channel = next((c for c in channels if c.name == channel_name), None)
    if not channel:
        channel = Channel(channel_name)
        channels.append(channel)
        client.socket.send(f'Channel {channel_name} has been created.\n'.encode())
    channel.clients.append(client)
    client.channel = channel

    join_message = f"You have joined channel: {channel.name}"
    client.socket.send(join_message.encode())
    broadcast(client.socket, f"SERVER: {client.nickname} has joined the channel.", channel)


def handle_leave(client, message):
    """Handles the /leave command."""
    if client.channel:
        channel_name = client.channel.name
        leave_message = f"You are leaving channel: {channel_name}"
        client.socket.send(leave_message.encode())
        broadcast(client.socket, f"SERVER: {client.nickname} has left the channel.", client.channel)
        client.channel.clients.remove(client)
        client.channel = None


def handle_nick(client, message):
    """Handles the /nick command."""
    new_nickname = message.split("/nick")[1].strip()
    if new_nickname:
        old_nickname = client.nickname
        client.nickname = new_nickname
        if client.channel:
            broadcast(client.socket, f"SERVER: {old_nickname} is now known as {client.nickname}.", client.channel)


def handle_list(client, message):
    """Handles the /list command."""
    if channels:
        channel_list = "Channels:\n" + "\n".join([f"{c.name} ({len(c.clients)} users)" for c in channels])
        client.socket.send(channel_list.encode())
    else:
        client.socket.send("No channels available.".encode())


def handle_msg(client, message):
    """Handles the /msg command."""
    try:
        parts = message.split()
        target_nickname = parts[1]
        private_message = " ".join(parts[2:])
        target_client = next((c for c in clients if c.nickname == target_nickname), None)
        if target_client:
            target_client.socket.send(f"PRIVATE MESSAGE from {client.nickname}: {private_message}".encode())
            client.socket.send(f"PRIVATE MESSAGE to {target_nickname}: {private_message}".encode())
        else:
            client.socket.send(f"SERVER: User {target_nickname} not found.".encode())
    except IndexError:
        client.socket.send("Invalid /msg command format. Usage: /msg <nickname> <message>".encode())


def handle_quit(client, message):
    """Handles the /quit command."""
    client.socket.send("Goodbye!".encode())


def handle_help(client, message):
    """Handles the /help command."""
    client.socket.send(help_msg.encode())
