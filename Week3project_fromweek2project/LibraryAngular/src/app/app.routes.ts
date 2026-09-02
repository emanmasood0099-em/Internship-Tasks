import { Routes } from '@angular/router';

import { BookList } from './book-list/book-list';
import { BookForm } from './book-form/book-form';

export const routes: Routes = [

  {
    path: 'books',
    component: BookList
  },

  {
    path: 'form',
    component: BookForm
  },

  {
    path: '',
    redirectTo: 'books',
    pathMatch: 'full'
  }

];