import { Component, ChangeDetectorRef } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Navigation } from './navigation/navigation';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    Navigation,
    FormsModule
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

  question = '';
  answer = '';
  loading = false;
  unavailable = false;

  constructor(private cdr: ChangeDetectorRef) {}

  async askQuestion() {

    if (!this.question.trim() || this.loading) {
      return;
    }

    this.answer = '';
    this.unavailable = false;
    this.loading = true;

    const questionText = this.question.trim();
    this.question = '';

    this.cdr.detectChanges();

    try {

      const response = await fetch(
        'http://localhost:5032/api/assistant/ask/stream',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream'
          },
          body: JSON.stringify({
            question: questionText
          })
        }
      );

      if (!response.ok) {
        throw new Error('AI service unavailable');
      }

      if (!response.body) {
        throw new Error('No streaming response received');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      let buffer = '';

      while (true) {

        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, {
          stream: true
        });

        const lines = buffer.split('\n');

        buffer = lines.pop() ?? '';

        for (const line of lines) {

          const trimmedLine = line.trim();

          if (trimmedLine.startsWith('data:')) {

            const data = trimmedLine.substring(5).trim();

            if (data && data !== '[DONE]') {
              this.answer += data + ' ';
              this.cdr.detectChanges();
            }
          }
        }
      }

      buffer += decoder.decode();

      const finalLines = buffer.split('\n');

      for (const line of finalLines) {

        const trimmedLine = line.trim();

        if (trimmedLine.startsWith('data:')) {

          const data = trimmedLine.substring(5).trim();

          if (data && data !== '[DONE]') {
            this.answer += data + ' ';
          }
        }
      }

      this.cdr.detectChanges();

    } catch (error) {

      console.error('AI streaming error:', error);

      this.unavailable = true;
      this.answer = '';

      this.cdr.detectChanges();

    } finally {

      this.loading = false;
      this.cdr.detectChanges();
    }
  }
}
