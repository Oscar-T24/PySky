import socket
import time

def ping_address(address, port):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the address and port
        sock.connect((address, port))
        print(f"Successfully connected to {address}:{port}")
        return 'True'
    except ConnectionRefusedError:
        print(f"Connection refused: Unable to connect to {address}:{port}")
    except socket.timeout:
        print(f"Connection timed out: Unable to connect to {address}:{port}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        sock.close()

# Usage example
while True:
    time.sleep(10)
    with open('etat.txt','w') as f:
        f.write(ping_address("93.14.22.225", 1025))  # Replace with the desired address and port


