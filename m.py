import zipfile
import os
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

def extract_zip(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        extract_path = file_path.replace('.zip', '')
        zip_ref.extractall(extract_path)
    return extract_path

def get_main_file_and_inputs(extract_path):
    main_file = None
    inputs = []
    for root, _, files in os.walk(extract_path):
        for file in files:
            if file.startswith('main.') and file.endswith(('.py', '.cpp', '.java')):
                main_file = os.path.join(root, file)
            elif file.startswith('input') and file.endswith('.txt'):
                with open(os.path.join(root, file), 'r') as input_file:
                    inputs.append(input_file.read().strip())
    return main_file, inputs

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    zip_file_path = '/Users/piyushsingh/Desktop/app/df/compiler-server/project-66a79e50b7e08d0fc727d04e.zip'
    
    # Extract the zip file
    extract_path = extract_zip(zip_file_path)
    
    # Get the main script file and inputs
    main_file, inputs_list = get_main_file_and_inputs(extract_path)
    
    if main_file:
        language = main_file.split('.')[-1]
        code = read_file(main_file)
        
        # Iterate over each input
        for input_data in inputs_list:
            result = send_code_to_lambda(language, code, [input_data])
            print(f"Output for input '{input_data}': {result}")
    else:
        print("No main script file found in the zip.")
