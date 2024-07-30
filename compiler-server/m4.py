import zipfile
import os
import shutil
import requests
import json

def send_code_to_lambda(language, code, inputs):
    url = "http://localhost:9090/2015-03-31/functions/function/invocations"
    
  
    payload = {
        "language": language,
        "code": code,
        "inputs": inputs
    }
    
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    
    
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
def ensure_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created output directory: {directory}")
    else:
        print(f"Output directory already exists: {directory}")
        
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
            elif file.startswith('input'):
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
    
    # Convert the output dictionary to a JSON string
    output_str = json.dumps(output, indent=4)
    
    # Define the output file path
    output_file_path = os.path.join(output_directory, f"{input_name}_output.txt")
    
    # Write the JSON string to the file
    with open(output_file_path, 'w') as output_file:
        output_file.write(output_str)

if __name__ == "__main__":
    print("Script started")
    code_repo_directory = '.'
    output_directory = 'outputs/'
    
    # Ensure output directory exists
    ensure_output_directory(output_directory)
    
    print(f"Looking for zip file in {code_repo_directory}")
    zip_file_path = find_zip_file(code_repo_directory)
    
    if zip_file_path:
        print(f"Zip file found: {zip_file_path}")
        extract_path = extract_zip(zip_file_path)
        print(f"Extracted to: {extract_path}")
        
        print("Searching for main file and inputs")
        main_file, inputs_list = get_main_file_and_inputs(extract_path)
        
        if main_file:
            print(f"Main file found: {main_file}")
            file_extension = main_file.split('.')[-1]
            language = get_language_from_extension(file_extension)
            
            if language == 'unsupported':
                print("Unsupported language:", file_extension)
            else:
                print(f"Language detected: {language}")
                code = read_file(main_file)
                
                print(f"Processing {len(inputs_list)} inputs")
                for index, input_data in enumerate(inputs_list):
                    print(f"Processing input {index + 1}: {input_data}")
                    result = send_code_to_lambda(language, code, [input_data])
                    input_name = f"input_{index + 1}"
                    save_output(result, output_directory, input_name)
                    print(f"Output for input '{input_data}': {result}")
                
                print(f"Cleaning up: removing {extract_path}")
                shutil.rmtree(extract_path)
        else:
            print("No main script file found in the zip.")
    else:
        print("No ZIP file found in the directory.")
    
    print("Script finished")