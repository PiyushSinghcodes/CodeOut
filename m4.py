import zipfile
import os
import shutil
import requests
import json

def send_code_to_lambda(language, code, inputs):
    url = "http://localhost:9090/2015-03-31/functions/function/invocations"
    
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

def get_language_from_extension(extension):
    language_map = {
        'py': 'python',
        'cpp': 'cpp',
        'java': 'java'
    }
    return language_map.get(extension, 'unsupported')

def find_zip_file(directory):
    for file in os.listdir(directory):
        if file.endswith(".zip"):
            return os.path.join(directory, file)
    return None

def save_output(output, output_directory, input_name):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_path = os.path.join(output_directory, f"{input_name}_output.txt")
    with open(output_file_path, 'w') as output_file:
        output_file.write(output)

if __name__ == "__main__":
    
    code_repo_directory = 'compiler-server/'
    
    
    zip_file_path = find_zip_file(code_repo_directory)
    
    if zip_file_path:
        
        extract_path = extract_zip(zip_file_path)
        
        
        main_file, inputs_list = get_main_file_and_inputs(extract_path)
        
        if main_file:
            file_extension = main_file.split('.')[-1]
            language = get_language_from_extension(file_extension)
            
            if language == 'unsupported':
                print("Unsupported language:", file_extension)
            else:
                code = read_file(main_file)
                output_directory = 'compiler-server/outputs'
                
               
                for index, input_data in enumerate(inputs_list):
                    result = send_code_to_lambda(language, code, [input_data])
                    input_name = f"input_{index + 1}"
                    save_output(result, output_directory, input_name)
                    print(f"Output for input '{input_data}': {result}")
                    
                
                shutil.rmtree(extract_path)
        else:
            print("No main script file found in the zip.")
    else:
        print("No ZIP file found in the directory.")
