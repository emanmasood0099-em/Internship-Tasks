import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface LoginResponse {
  token: string;
  username: string;
  role: string;
}

@Injectable({
  providedIn: 'root'
})
export class Auth {

  private apiUrl = 'http://localhost:5032/api/Auth';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(
      `${this.apiUrl}/login`,
      {
        username,
        password
      }
    );
  }

  saveSession(response: LoginResponse): void {
    localStorage.setItem('token', response.token);
    localStorage.setItem('username', response.username);
    localStorage.setItem('role', response.role);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  getUsername(): string | null {
    return localStorage.getItem('username');
  }

  getRole(): string | null {
    return localStorage.getItem('role');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  isAdmin(): boolean {
    return this.getRole() === 'Admin';
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
  }
}