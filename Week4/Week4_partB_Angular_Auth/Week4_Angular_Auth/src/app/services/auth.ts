import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private token: string | null = localStorage.getItem('token');

  login(username: string, password: string): Observable<any> {

    // Admin user
    if (username === 'admin' && password === '1234') {

      const demoToken =
        'eyJhbGciOiJIUzI1NiJ9.' +
        btoa(JSON.stringify({
          username: 'admin',
          role: 'Admin'
        })) +
        '.partBdemo';

      this.token = demoToken;
      localStorage.setItem('token', demoToken);

      return of({
        token: demoToken
      });
    }

    // Non-Admin user
    if (username === 'user' && password === '1234') {

      const demoToken =
        'eyJhbGciOiJIUzI1NiJ9.' +
        btoa(JSON.stringify({
          username: 'user',
          role: 'User'
        })) +
        '.partBdemo';

      this.token = demoToken;
      localStorage.setItem('token', demoToken);

      return of({
        token: demoToken
      });
    }

    // Invalid login
    return of({
      token: null
    });
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('token');
  }

  getToken(): string | null {
    return this.token;
  }

  isLoggedIn(): boolean {
    return this.token !== null;
  }
}