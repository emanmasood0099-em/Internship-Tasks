import { Component } from '@angular/core';

export interface Student {
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
}