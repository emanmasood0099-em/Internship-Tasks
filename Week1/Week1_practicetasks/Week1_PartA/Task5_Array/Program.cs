int[] numbers = { 25, 10, 45, 5, 80, 30, 15, 60, 90, 20 };

int largest = numbers[0];
int smallest = numbers[0];

for (int i = 1; i < numbers.Length; i++)
{
    if (numbers[i] > largest)
    {
        largest = numbers[i];
    }

    if (numbers[i] < smallest)
    {
        smallest = numbers[i];
    }
}

Console.WriteLine("Numbers in the array:");

for (int i = 0; i < numbers.Length; i++)
{
    Console.Write(numbers[i] + " ");
}

Console.WriteLine();
Console.WriteLine("Largest number = " + largest);
Console.WriteLine("Smallest number = " + smallest);