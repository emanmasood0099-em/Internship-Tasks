Console.Write("Enter first number: ");
double number1 = Convert.ToDouble(Console.ReadLine());

Console.Write("Enter second number: ");
double number2 = Convert.ToDouble(Console.ReadLine());

double sum = number1 + number2;
double difference = number1 - number2;
double product = number1 * number2;
double quotient = number1 / number2;

Console.WriteLine();
Console.WriteLine("----- Results -----");
Console.WriteLine("Sum = " + sum);
Console.WriteLine("Difference = " + difference);
Console.WriteLine("Product = " + product);
Console.WriteLine("Quotient = " + quotient);