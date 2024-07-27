import subprocess
import tempfile
import os

def execute_python(code, user_inputs=None):
    if user_inputs is None:
        user_inputs = []

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode())
            temp_file.flush()
            temp_filename = temp_file.name

        input_str = "\n".join(user_inputs)

        result = subprocess.run(
            ['python3', temp_filename],
            input=input_str.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output = result.stdout.decode().strip()
        error = result.stderr.decode().strip()

        if result.returncode == 0:
            return output
        else:
            return f"Error: {error}"

    except Exception as e:
        return str(e)
    finally:
        os.remove(temp_filename)

def execute_java(code, user_inputs=None):
    try:
        if user_inputs is None:
            user_inputs = []

        with open('/tmp/Main.java', 'w') as java_file:
            java_file.write(code)

        compile_result = subprocess.run(
            ['javac', '/tmp/Main.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if compile_result.returncode != 0:
            return {
                'statusCode': 400,
                'body': f"Compilation failed: {compile_result.stderr.decode()}"
            }

        input_str = "\n".join(user_inputs)

        run_result = subprocess.run(
            ['java', '-classpath', '/tmp', 'Main'],
            input=input_str.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if run_result.returncode != 0:
            return {
                'statusCode': 400,
                'body': f"Runtime error: {run_result.stderr.decode()}"
            }

        output = run_result.stdout.decode().strip()

        return {
            'statusCode': 200,
            'body': output
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Exception: {str(e)}"
        }

def execute_cpp(code, user_inputs=None):
    try:
        if user_inputs is None:
            user_inputs = []

        with open('/tmp/temp.cpp', 'w') as cpp_file:
            cpp_file.write(code)

        compile_result = subprocess.run(
            ['g++', '/tmp/temp.cpp', '-o', '/tmp/temp'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if compile_result.returncode != 0:
            return f"Compilation failed: {compile_result.stderr.decode()}"

        input_str = "\n".join(user_inputs)

        run_result = subprocess.run(
            ['/tmp/temp'],
            input=input_str.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return run_result.stdout.decode() + run_result.stderr.decode()

    except Exception as e:
        return str(e)
event={
    "language": "python",
    "code": "print('Hello, ' + input('Enter your name: '))",
    "inputs": ["Alice"]
}

def handler(event, context=None):
    language = event.get('language', 'python')
    code = event.get('code', '')
    user_inputs = event.get('inputs', [])

    if language == 'python':
        res = execute_python(code, user_inputs)
    elif language == 'java':
        res = execute_java(code, user_inputs)
    elif language == 'cpp':
        res = execute_cpp(code, user_inputs)
    else:
        res = f'Unsupported Language: {language}'
    
    print(res)
    return {
        'statusCode': 200,
        'body': res
    }
