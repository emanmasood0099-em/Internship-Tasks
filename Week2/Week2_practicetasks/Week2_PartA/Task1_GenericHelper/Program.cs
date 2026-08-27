static void PrintValue<T>(T value)
{
    Console.WriteLine("Value: " + value);
}

PrintValue<int>(100);
PrintValue<string>("Hello C#");
PrintValue<double>(25.5);
PrintValue<bool>(true);