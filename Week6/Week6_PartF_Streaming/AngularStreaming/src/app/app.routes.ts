import { Component } from '@angular/core';
import { Routes } from '@angular/router';
import { App } from './app';

@Component({
  selector: 'app-test-page',
  standalone: true,
  template: `
    <div style="padding: 40px;">
      <h1>Test Page</h1>
      <p>You navigated away from the streaming page.</p>
    </div>
  `
})
class TestPage {}

export const routes: Routes = [
  {
    path: '',
    component: App
  },
  {
    path: 'test',
    component: TestPage
  }
];