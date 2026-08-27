Console.Write("Enter your marks: ");

int marks = Convert.ToInt32(Console.ReadLine());

string grade = GetGrade(marks);

Console.WriteLine("Your Grade is: " + grade);

static string GetGrade(int marks)
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