using StudentManagement.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace StudentManagement.Services
{
    public class StudentManager
    {
        private List<Student> students = new List<Student>();

        // ADD
        public void AddStudent(Student student)
        {
            students.Add(student);
            Console.WriteLine("Student added successfully!");
        }

        // VIEW
        public void ViewStudents()
        {
            if (students.Count == 0)
            {
                Console.WriteLine("No students found.");
                return;
            }

            Console.WriteLine("\n--- Student List ---");

            foreach (Student student in students)
            {
                Console.WriteLine(
                    $"ID: {student.Id}, Name: {student.Name}, Email: {student.Email}, Age: {student.Age}"
                );
            }
        }

        // SEARCH using LINQ
        public void SearchStudent(string name)
        {
            var result = students
                .Where(s => s.Name.ToLower().Contains(name.ToLower()))
                .ToList();

            if (result.Count == 0)
            {
                Console.WriteLine("Student not found.");
                return;
            }

            Console.WriteLine("\n--- Search Results ---");

            foreach (Student student in result)
            {
                Console.WriteLine(
                    $"ID: {student.Id}, Name: {student.Name}, Email: {student.Email}, Age: {student.Age}"
                );
            }
        }

        // UPDATE
        public void UpdateStudent(int id, string name, string email, int age)
        {
            Student student = students.FirstOrDefault(s => s.Id == id);

            if (student == null)
            {
                Console.WriteLine("Student not found.");
                return;
            }

            student.Name = name;
            student.Email = email;
            student.Age = age;

            Console.WriteLine("Student updated successfully!");
        }

        // DELETE
        public void DeleteStudent(int id)
        {
            Student student = students.FirstOrDefault(s => s.Id == id);

            if (student == null)
            {
                Console.WriteLine("Student not found.");
                return;
            }

            students.Remove(student);

            Console.WriteLine("Student deleted successfully!");
        }

        // SORT using LINQ
        public void SortStudents()
        {
            var sortedStudents = students
                .OrderBy(s => s.Name)
                .ToList();

            Console.WriteLine("\n--- Students Sorted by Name ---");

            foreach (Student student in sortedStudents)
            {
                Console.WriteLine(
                    $"ID: {student.Id}, Name: {student.Name}, Email: {student.Email}, Age: {student.Age}"
                );
            }
        }
    }
}