try
{
    Console.Write("Enter your age: ");

    int age = Convert.ToInt32(Console.ReadLine());

    Console.WriteLine("Your age is: " + age);
}
catch
{
    Console.WriteLine("Invalid input. Please enter a number.");
}