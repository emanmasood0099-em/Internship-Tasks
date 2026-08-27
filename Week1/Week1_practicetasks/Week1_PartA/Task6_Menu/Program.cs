while (true)
{
    Console.WriteLine();
    Console.WriteLine("===== MENU =====");
    Console.WriteLine("1. Add Two Numbers");
    Console.WriteLine("2. Subtract Two Numbers");
    Console.WriteLine("3. Multiply Two Numbers");
    Console.WriteLine("4. Exit");
    Console.Write("Enter your choice: ");

    int choice = Convert.ToInt32(Console.ReadLine());

    if (choice == 4)
    {
        Console.WriteLine("Program exited.");
        break;
    }

    if (choice >= 1 && choice <= 3)
    {
        Console.Write("Enter first number: ");
        int num1 = Convert.ToInt32(Console.ReadLine());

        Console.Write("Enter second number: ");
        int num2 = Convert.ToInt32(Console.ReadLine());

        if (choice == 1)
        {
            Console.WriteLine("Result = " + (num1 + num2));
        }
        else if (choice == 2)
        {
            Console.WriteLine("Result = " + (num1 - num2));
        }
        else if (choice == 3)
        {
            Console.WriteLine("Result = " + (num1 * num2));
        }
    }
    else
    {
        Console.WriteLine("Invalid choice. Please try again.");
    }
}