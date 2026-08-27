List<Student> students = new List<Student>();

students.Add(new Student(101, "Ali"));
students.Add(new Student(102, "Sara"));
students.Add(new Student(103, "Ahmed"));
students.Add(new Student(104, "Fatima"));
students.Add(new Student(105, "Usman"));

int searchId = 103;

var student = students.FirstOrDefault(s => s.Id == searchId);

if (student != null)
{
    Console.WriteLine("Student Found");
    Console.WriteLine("ID: " + student.Id);
    Console.WriteLine("Name: " + student.Name);
}
else
{
    Console.WriteLine("Student not found.");
}