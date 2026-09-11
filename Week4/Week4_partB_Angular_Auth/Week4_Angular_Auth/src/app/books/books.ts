
import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

import { AuthService } from '../services/auth';

@Component({
  selector: 'app-books',
  imports: [],
  templateUrl: './books.html',
  styleUrl: './books.css'
})
export class Books {

  isAdmin: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private http: HttpClient
  ) {
    this.checkAdminRole();
  }

  checkAdminRole(): void {
    const token = this.authService.getToken();

    if (!token) {
      this.isAdmin = false;
      return;
    }

    try {
      const payload = token.split('.')[1];
      const decodedPayload = JSON.parse(atob(payload));

      this.isAdmin = decodedPayload.role === 'Admin';
    } catch {
      this.isAdmin = false;
    }
  }

  addBook(): void {

    const book = {
      title: 'Angular Authentication',
      author: 'Internship Practice'
    };

    this.http.post('http://localhost:5165/api/books', book).subscribe({
      next: () => {
        alert('Book created successfully!');
      },
      error: () => {
        alert('Book creation request sent.');
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
