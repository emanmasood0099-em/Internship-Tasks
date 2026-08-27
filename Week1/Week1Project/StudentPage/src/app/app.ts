import { Component } from '@angular/core';
import { StudentList } from './student-list/student-list';

@Component({
  selector: 'app-root',
  imports: [StudentList],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
}