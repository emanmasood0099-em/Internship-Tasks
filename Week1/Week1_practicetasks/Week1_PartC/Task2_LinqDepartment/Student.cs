public class Student
{
    public string Name { get; set; }
    public string Department { get; set; }

    public Student(string name, string department)
    {
        Name = name;
        Department = department;
    }
}