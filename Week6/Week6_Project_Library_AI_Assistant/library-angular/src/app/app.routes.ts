import { Routes } from '@angular/router';

import { BookList } from './book-list/book-list';
import { BookForm } from './book-form/book-form';
import { Login } from './login/login';
import { authGuard } from './auth-guard';

export const routes: Routes = [
  {
    path: 'login',
    component: Login
  },
  {
    path: 'books',
    component: BookList,
    canActivate: [authGuard]
  },
  {
    path: 'form',
    component: BookForm,
    canActivate: [authGuard]
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  }
];