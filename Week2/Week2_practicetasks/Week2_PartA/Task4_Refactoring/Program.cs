
/*mess
Console.Write("Enter student name: ");
string name = Console.ReadLine()!;

Console.Write("Enter marks: ");
int marks = Convert.ToInt32(Console.ReadLine());

string grade;

if (marks >= 80)
{
    grade = "A";
}
else if (marks >= 70)
{
    grade = "B";
}
else if (marks >= 60)
{
    grade = "C";
}
else if (marks >= 50)
{
    grade = "D";
}
else
{
    grade = "F";
}

Console.WriteLine();
Console.WriteLine("----- Student Result -----");
Console.WriteLine("Student Name: " + name);
Console.WriteLine("Marks: " + marks);
Console.WriteLine("Grade: " + grade);
*/


//Refactored 

using System;

class Program
{
    static void Main()
    {
        string name = GetStudentName();
        int marks = GetMarks();
        string grade = CalculateGrade(marks);

        DisplayResult(name, marks, grade);
    }

    static string GetStudentName()
    {
        Console.Write("Enter student name: ");
        return Console.ReadLine()!;
    }

    static int GetMarks()
    {
        Console.Write("Enter marks: ");
        return Convert.ToInt32(Console.ReadLine());
    }

    static string CalculateGrade(int marks)
    {
        if (marks >= 80)
        {
            return "A";
        }
        else if (marks >= 70)
        {
            return "B";
        }
        else if (marks >= 60)
        {
            return "C";
        }
        else if (marks >= 50)
        {
            return "D";
        }
        else
        {
            return "F";
        }
    }

    static void DisplayResult(string name, int marks, string grade)
    {
        Console.WriteLine();
        Console.WriteLine("----- Student Result -----");
        Console.WriteLine("Student Name: " + name);
        Console.WriteLine("Marks: " + marks);
        Console.WriteLine("Grade: " + grade);
    }
}