import socket
import re
import time

HOST = 'challenges.alphabit.club'
PORT = 1314

def recv_until(s, delim):
    data = b""
    delim_bytes = delim.encode()
    while delim_bytes not in data:
        chunk = s.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode()

def get_prediction(s, inputs):
    query_str = " ".join(map(str, inputs)) + "\n"
    s.sendall(query_str.encode())
    response = recv_until(s, '$')
    match = re.search(r'Prediction:\s*(-?\d+)', response)
    if match:
        return int(match.group(1))
    else:
        print("Failed to parse prediction from response:")
        print(response)
        return None

def main():
    print(f"Connecting to {HOST}:{PORT} ...")
    s = socket.create_connection((HOST, PORT))
    banner = s.recv(1024).decode()
    print("Server banner:")
    print(banner)
    time.sleep(0.5)  
    zeros = [0] * 25
    print("Sending baseline input (all zeros)...")
    baseline = get_prediction(s, zeros)
    if baseline is None:
        print("Could not get baseline prediction. Exiting.")
        s.close()
        return
    print(f"Baseline (bias) b = {baseline}")
    weights = []
    for i in range(25):
        vec = [0] * 25
        vec[i] = 1  # set the i-th feature to 1
        print(f"Sending input with a 1 at index {i} ...")
        pred = get_prediction(s, vec)
        if pred is None:
            print(f"Failed to get prediction for index {i}.")
            weights.append(None)
        else:
            weight = pred - baseline
            weights.append(weight)
            print(f"  -> Weight w[{i}] = {weight}")

    print("\nExtracted weights:")
    for idx, wt in enumerate(weights):
        print(f"w[{idx}] = {wt}")
    try:
        ascii_chars = [chr(wt) for wt in weights]
        flag = "".join(ascii_chars)
        print("\nFlag:")
        print(flag)
    except Exception as e:
        print("Error converting weights to ASCII characters:", e)

    s.close()

if __name__ == '__main__':
    main()
