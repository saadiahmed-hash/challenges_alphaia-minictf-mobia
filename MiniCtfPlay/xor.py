import socket

def connect_and_receive():
    host = "challenges.alphabit.club"
    port = 1314
    
    try:
        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((host, port))
            
            # Receive the response
            response = s.recv(1024)  # Adjust buffer size as needed
            
            # Print the response
            print(response.decode())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    connect_and_receive()
