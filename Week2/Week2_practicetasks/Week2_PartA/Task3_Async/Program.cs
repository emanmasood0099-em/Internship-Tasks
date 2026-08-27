using System;
using System.Threading.Tasks;

class Program
{
    static async Task<string> GetMessageAsync()
    {
        Console.WriteLine("Waiting for result...");

        await Task.Delay(3000);

        return "Result received successfully!";
    }

    static async Task Main()
    {
        string result = await GetMessageAsync();

        Console.WriteLine(result);
    }
}