import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {
  ReactiveFormsModule,
  FormBuilder,
  Validators
} from '@angular/forms';
import { Book, BookService } from './services/book.service';

@Component({
  imports: [RouterOutlet, ReactiveFormsModule],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App implements OnInit {

  books: Book[] = [];

  isLoading = false;
  isSaving = false;

  errorMessage = '';
  postErrorMessage = '';
  successMessage = '';

  bookForm;

  constructor(
    private bookService: BookService,
    private fb: FormBuilder,
    private cdr: ChangeDetectorRef
  ) {
    this.bookForm = this.fb.group({
      title: ['', Validators.required],
      author: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.bookService.getBooks().subscribe({

      next: (books) => {
        console.log('BOOKS RECEIVED:', books);

        this.books = books;
        this.isLoading = false;

        this.cdr.detectChanges();
      },

      error: (err) => {
        console.error('GET API ERROR:', err);

        this.errorMessage = 'Could not load books.';
        this.isLoading = false;

        this.cdr.detectChanges();
      }

    });
  }

  addBook(): void {

    if (this.bookForm.invalid) {
      this.bookForm.markAllAsTouched();
      return;
    }

    this.isSaving = true;
    this.postErrorMessage = '';
    this.successMessage = '';

    const book = {
      title: this.bookForm.value.title!,
      author: this.bookForm.value.author!
    };

    console.log('BOOK TO SEND:', book);

    this.bookService.addBook(book).subscribe({

      next: (createdBook) => {
        console.log('BOOK CREATED:', createdBook);

        this.isSaving = false;
        this.successMessage = 'Book added successfully!';

        this.bookForm.reset();

        this.cdr.detectChanges();

        this.loadBooks();
      },

      error: (err) => {
        console.error('POST API ERROR:', err);

        this.isSaving = false;
        this.postErrorMessage = 'Could not add book.';

        this.cdr.detectChanges();
      }

    });
  }
}