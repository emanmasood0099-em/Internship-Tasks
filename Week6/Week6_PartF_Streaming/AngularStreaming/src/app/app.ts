import {
  ChangeDetectorRef,
  Component,
  HostListener,
  OnDestroy
} from '@angular/core';

import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnDestroy {

  question = '';
  answer = '';
  loading = false;

  private abortController: AbortController | null = null;

  constructor(
    private changeDetector: ChangeDetectorRef
  ) {}

  async askQuestion(): Promise<void> {

    if (!this.question.trim()) {
      return;
    }

    this.answer = '';
    this.loading = true;

    this.abortController = new AbortController();

    this.changeDetector.detectChanges();

    try {

      const response = await fetch(
        'http://localhost:5173/api/assistant/ask/stream',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            question: this.question
          }),
          signal: this.abortController.signal
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      if (!response.body) {
        throw new Error(
          'Streaming response body is not available.'
        );
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = '';

      while (true) {

        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, {
          stream: true
        });

        const events = buffer.split('\n\n');

        buffer = events.pop() ?? '';

        for (const event of events) {

          const lines = event.split('\n');

          for (const line of lines) {

            if (!line.startsWith('data: ')) {
              continue;
            }

            const text = line.slice(6).trim();

            if (text === '[DONE]') {
              return;
            }

            this.answer += text + ' ';

            this.changeDetector.detectChanges();
          }
        }
      }

    } catch (error) {

      if (
        error instanceof DOMException &&
        error.name === 'AbortError'
      ) {
        console.log(
          'Streaming request cancelled because the user navigated away.'
        );

        return;
      }

      console.error(
        'Streaming error:',
        error
      );

      this.answer = 'Unable to get AI response.';

      this.changeDetector.detectChanges();

    } finally {

      this.loading = false;
      this.abortController = null;

      this.changeDetector.detectChanges();
    }
  }

  @HostListener('window:pagehide')
  onPageHide(): void {

    if (this.abortController) {

      console.log(
        'Page left. Aborting streaming request.'
      );

      this.abortController.abort();

      this.abortController = null;
    }
  }

  ngOnDestroy(): void {

    if (this.abortController) {

      console.log(
        'Component destroyed. Aborting streaming request.'
      );

      this.abortController.abort();

      this.abortController = null;
    }
  }
}