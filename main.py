import requests
import json

def send_code_to_lambda(language, code, inputs):
    url = "http://localhost:900/2015-03-31/functions/function/invocations"
    
    # Create the payload
    payload = {
        "language": language,
        "code": code,
        "inputs": inputs
    }
    
    # Send the POST request
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    
    # Check if the response was successful
    if response.status_code == 200:
        response_data = response.json()
        if 'body' in response_data:
            return response_data['body']
        else:
            return "Error: 'body' not found in the response"
    else:
        return {
            'statusCode': response.status_code,
            'body': response.text
        }

if __name__ == "__main__":
    language = "python"
    code = """
def main():
    name = input("Enter your name: ")
    print(f"Hello, {name}")

if __name__ == "__main__":
    main()
"""
    # Multiple sets of inputs
    inputs_list = [
        ["Alice"],
        ["Bob"],
        ["Charlie"]
    ]
    
    # Iterate over each set of inputs
    for inputs in inputs_list:
        result = send_code_to_lambda(language, code, inputs)
        print("Output for inputs", inputs, ":", result)
