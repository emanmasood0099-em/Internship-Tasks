import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Auth } from '../auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {

  loginForm: FormGroup;
  message = '';

  constructor(
    private fb: FormBuilder,
    private auth: Auth,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  login(): void {
    if (this.loginForm.invalid) {
      this.message = 'Please enter username and password.';
      return;
    }

    const username = this.loginForm.value.username;
    const password = this.loginForm.value.password;

    this.auth.login(username, password).subscribe({
      next: (response) => {
        this.auth.saveSession(response);
        this.message = 'Login successful!';
        this.router.navigate(['/books']);
      },
      error: () => {
        this.message = 'Invalid username or password.';
      }
    });
  }
}