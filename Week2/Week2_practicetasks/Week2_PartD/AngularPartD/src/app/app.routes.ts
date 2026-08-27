import { Routes } from '@angular/router';
import { Students } from './students/students';
import { Registration } from './registration/registration';

export const routes: Routes = [
  {
    path: 'students',
    component: Students
  },
  {
    path: 'registration',
    component: Registration
  },
  {
    path: '',
    redirectTo: 'students',
    pathMatch: 'full'
  }
];