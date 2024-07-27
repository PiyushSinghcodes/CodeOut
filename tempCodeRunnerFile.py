if __name__ == "__main__":
    language = "java"
    code = """
import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a number: ");
        int num1 = scanner.nextInt();
        System.out.print("Enter another number: ");
        int num2 = scanner.nextInt();
        
        int sum = num1 + num2;
        System.out.println("The sum is: " + sum);

        scanner.close();
    }
}
"""
    inputs = ["5", "7"]