import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class StudentService {

  students = [
    {
      id: 1,
      name: 'Ali',
      email: 'ali@gmail.com'
    },
    {
      id: 2,
      name: 'Sara',
      email: 'sara@gmail.com'
    },
    {
      id: 3,
      name: 'Ahmed',
      email: 'ahmed@gmail.com'
    }
  ];

  getStudents() {
    return this.students;
  }
}