List<Student> students = new List<Student>();

students.Add(new Student("Eman", 75));
students.Add(new Student("Sara", 90));
students.Add(new Student("Ahmed", 60));
students.Add(new Student("Fatima", 85));
students.Add(new Student("Usman", 70));

var sortedStudents = students.OrderBy(student => student.Marks);

Console.WriteLine("Students sorted by marks:");

foreach (var student in sortedStudents)
{
    Console.WriteLine(student.Name + " - " + student.Marks);
}