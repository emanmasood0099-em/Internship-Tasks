import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentService } from '../student';

@Component({
  selector: 'app-students',
  imports: [CommonModule],
  templateUrl: './students.html',
  styleUrl: './students.css'
})
export class Students {

  students: any[] = [];

  constructor(private studentService: StudentService) {
    this.students = this.studentService.getStudents();
  }
}