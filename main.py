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
# if __name__ == "__main__":
#     language = "python"
#     code = """
# def main():
#     name = input("Enter your name: ")
#     print(f"Hello, {name}")

# if __name__ == "__main__":
#     main()
# """
#     inputs = ["Alice"]
        


 # Example usage for C++
# if __name__ == "__main__":
#     language = "cpp"
#     code = """
# #include <iostream>
# using namespace std;

# int main() {
#     string name;
#     cout << "Enter your name: ";
#     cin >> name;
#     cout << "Hello, " << name << endl;
#     return 0;
# }
# """
#     inputs = ["Alice"]       

# Example usage for Java with inputs
# if __name__ == "__main__":
#     language = "java"
#     code = """
# import java.util.Scanner;

# class Main {
#     public static void main(String[] args) {
#         Scanner scanner = new Scanner(System.in);

#         System.out.print("Enter a number: ");
#         int num1 = scanner.nextInt();
#         System.out.print("Enter another number: ");
#         int num2 = scanner.nextInt();
        
#         int sum = num1 + num2;
#         System.out.println("The sum is: " + sum);

#         scanner.close();
#     }
# }
# """
#     inputs = ["5", "7"]
    
    result = send_code_to_lambda(language, code, inputs)
    print("Output", result)
