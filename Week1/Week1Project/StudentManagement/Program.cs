using StudentManagement.Models;
using StudentManagement.Services;

StudentManager manager = new StudentManager();

while (true)
{
    Console.WriteLine("\n==============================");
    Console.WriteLine("   STUDENT MANAGEMENT SYSTEM");
    Console.WriteLine("==============================");
    Console.WriteLine("1. Add Student");
    Console.WriteLine("2. View Students");
    Console.WriteLine("3. Search Student");
    Console.WriteLine("4. Update Student");
    Console.WriteLine("5. Delete Student");
    Console.WriteLine("6. Sort Students");
    Console.WriteLine("7. Exit");
    Console.WriteLine("==============================");

    Console.Write("Enter your choice: ");

    try
    {
        int choice = int.Parse(Console.ReadLine()!);

        switch (choice)
        {
            case 1:
                AddStudent(manager);
                break;

            case 2:
                manager.ViewStudents();
                break;

            case 3:
                Console.Write("Enter student name to search: ");
                string searchName = Console.ReadLine()!;

                manager.SearchStudent(searchName);
                break;

            case 4:
                UpdateStudent(manager);
                break;

            case 5:
                Console.Write("Enter student ID to delete: ");
                int deleteId = int.Parse(Console.ReadLine()!);

                manager.DeleteStudent(deleteId);
                break;

            case 6:
                manager.SortStudents();
                break;

            case 7:
                Console.WriteLine("Thank you for using Student Management System!");
                return;

            default:
                Console.WriteLine("Invalid choice. Please select 1-7.");
                break;
        }
    }
    catch (FormatException)
    {
        Console.WriteLine("Invalid input! Please enter a number.");
    }
    catch (Exception ex)
    {
        Console.WriteLine("Error: " + ex.Message);
    }
}

static void AddStudent(StudentManager manager)
{
    try
    {
        Console.Write("Enter Student ID: ");
        int id = int.Parse(Console.ReadLine()!);

        Console.Write("Enter Student Name: ");
        string name = Console.ReadLine()!;

        Console.Write("Enter Student Email: ");
        string email = Console.ReadLine()!;

        Console.Write("Enter Student Age: ");
        int age = int.Parse(Console.ReadLine()!);

        Student student = new Student(id, name, email, age);

        manager.AddStudent(student);
    }
    catch (FormatException)
    {
        Console.WriteLine("Invalid input! ID and Age must be numbers.");
    }
}

static void UpdateStudent(StudentManager manager)
{
    try
    {
        Console.Write("Enter Student ID to update: ");
        int id = int.Parse(Console.ReadLine()!);

        Console.Write("Enter new name: ");
        string name = Console.ReadLine()!;

        Console.Write("Enter new email: ");
        string email = Console.ReadLine()!;

        Console.Write("Enter new age: ");
        int age = int.Parse(Console.ReadLine()!);

        manager.UpdateStudent(id, name, email, age);
    }
    catch (FormatException)
    {
        Console.WriteLine("Invalid input! ID and Age must be numbers.");
    }
}