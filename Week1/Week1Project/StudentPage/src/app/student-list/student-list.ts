import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { StudentCard } from '../student-card/student-card';

@Component({
  selector: 'app-student-list',
  imports: [FormsModule, StudentCard],
  templateUrl: './student-list.html',
  styleUrl: './student-list.css'
})
export class StudentList {

  students = [
    {
      id: 1,
      name: 'Ali',
      email: 'ali@gmail.com',
      age: 20
    },
    {
      id: 2,
      name: 'Sara',
      email: 'sara@gmail.com',
      age: 21
    },
    {
      id: 3,
      name: 'Ahmed',
      email: 'ahmed@gmail.com',
      age: 19
    }
  ];

  searchText = '';

  get filteredStudents() {
    return this.students.filter(student =>
      student.name.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }
}