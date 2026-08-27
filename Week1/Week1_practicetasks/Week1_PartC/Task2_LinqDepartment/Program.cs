List<Student> students = new List<Student>();

students.Add(new Student("Eman", "Software Engineering"));
students.Add(new Student("Sara", "Software Engineering"));
students.Add(new Student("Ahmed", "Computer Science"));
students.Add(new Student("Fatima", "Information Technology"));
students.Add(new Student("Usman", "Computer Science"));

var csStudents = students.Where(student => student.Department == "Software Engineering");

Console.WriteLine("Software Engineering Students:");

foreach (var student in csStudents)
{
    Console.WriteLine(student.Name);
}