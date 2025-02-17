import socket

HOST = 'localhost'
PORT = 1337

def read_line(sock):
    buffer = b''
    while True:
        chunk = sock.recv(1)  # Read byte by byte
        if not chunk:
            break
        buffer += chunk
        if buffer.endswith(b'\n'):
            break
    return buffer.decode().strip()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    # Clear initial server messages
    while True:
        line = read_line(s)
        if 'Enter inputs' in line:
            break
    
    # Get bias with all-zero input
    zero_input = '0 ' * 25 + '\n'
    s.sendall(zero_input.encode())
    bias_line = read_line(s)
    bias = int(bias_line.split()[1])
    
    # Retrieve each weight
    weights = []
    for i in range(25):
        input_vec = [0] * 25
        input_vec[i] = 1
        input_str = ' '.join(map(str, input_vec)) + '\n'
        s.sendall(input_str.encode())
        
        response = read_line(s)
        prediction = int(response.split()[1])
        weights.append(prediction - bias)
    
    # Convert weights to flag
    flag = ''.join(chr(w) for w in weights)
    print("Flag:", flag)