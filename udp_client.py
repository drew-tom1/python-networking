import socket
from log_message import LogMessage
import sys
import zlib

def send_log_udp(log_message):
    # Message is encoded into bytes
    object_bytes = LogMessage.to_bytes(log_message)
    
    final_bytes = LogMessage.add_header(object_bytes)

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # current server address refers to local testing and experimentation
        server_address = ('localhost', 12345)

        # Send the serialized message to the server - already in bytes
        client_socket.sendto(final_bytes, server_address)

        # Receive the response from the server
        modified_message, _ = client_socket.recvfrom(1024)

        # Print the modified message received from the server
        print(f"Received from server: {modified_message.decode()}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    # Check if any command-line argument is provided
    if len(sys.argv) > 1:
        # Take the first command-line argument as the message
        message = sys.argv[1]
    else:
        # If no argument is provided, prompt the user for input
        message = input("Enter a message: ")

    # Create a LogMessage instance with a default header
    log_message = LogMessage("System Log", message, "Info", "example.py", 42)

    # Send the serialized LogMessage to the server
    send_log_udp(log_message)
