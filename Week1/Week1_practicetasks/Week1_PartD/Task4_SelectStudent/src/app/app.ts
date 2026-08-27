import { Component } from '@angular/core';

interface Student {
  id: number;
  name: string;
  department: string;
  marks: number;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

  students: Student[] = [
    {
      id: 101,
      name: 'Eman',
      department: 'Software Engineering',
      marks: 85
    },
    {
      id: 102,
      name: 'Sara',
      department: 'Software Engineering',
      marks: 90
    },
    {
      id: 103,
      name: 'Ahmed',
      department: 'Computer Science',
      marks: 75
    },
    {
      id: 104,
      name: 'Fatima',
      department: 'Information Technology',
      marks: 88
    },
    {
      id: 105,
      name: 'Usman',
      department: 'Computer Science',
      marks: 70
    }
  ];

  selectedStudent: Student | null = null;

  selectStudent(student: Student) {
    this.selectedStudent = student;
  }
}