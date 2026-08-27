public class Teacher : Person, IPrintable
{
    public string Subject { get; set; }

    public Teacher(string name, int age, string subject)
        : base(name, age)
    {
        Subject = subject;
    }

    public void PrintInfo()
    {
        Console.WriteLine("Teacher Information");
        Console.WriteLine("Name: " + Name);
        Console.WriteLine("Age: " + Age);
        Console.WriteLine("Subject: " + Subject);
    }
}