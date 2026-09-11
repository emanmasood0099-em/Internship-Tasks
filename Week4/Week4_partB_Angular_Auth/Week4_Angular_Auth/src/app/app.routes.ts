import { Routes } from '@angular/router';

import { authGuard } from './guards/auth-guard';
import { Login } from './login/login';
import { Books } from './books/books';

export const routes: Routes = [
  {
    path: 'login',
    component: Login
  },
  {
    path: 'books',
    canActivate: [authGuard],
    component: Books
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  }
];