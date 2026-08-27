public class Student : Person, IPrintable
{
    public string StudentId { get; set; }

    public Student(string name, int age, string studentId)
        : base(name, age)
    {
        StudentId = studentId;
    }

    public void PrintInfo()
    {
        Console.WriteLine("Student Information");
        Console.WriteLine("Name: " + Name);
        Console.WriteLine("Age: " + Age);
        Console.WriteLine("Student ID: " + StudentId);
    }
}