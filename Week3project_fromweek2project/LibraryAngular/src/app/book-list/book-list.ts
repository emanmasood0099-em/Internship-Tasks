import {
  Component,
  EventEmitter,
  OnInit,
  Output,
  ChangeDetectorRef
} from '@angular/core';

import { BookService, Book } from '../book';

@Component({
  selector: 'app-book-list',
  imports: [],
  templateUrl: './book-list.html',
  styleUrl: './book-list.css'
})
export class BookList implements OnInit {

  @Output() editBook = new EventEmitter<Book>();

  books: Book[] = [];

  isLoading = false;

  errorMessage = '';

  constructor(
    private bookService: BookService,
    private cdr: ChangeDetectorRef
  ) {
    console.log('BookList component created');
  }

  ngOnInit(): void {
    console.log('BookList started');

    this.loadBooks();
  }

  loadBooks(): void {

    console.log('Loading books from API...');

    this.isLoading = true;
    this.errorMessage = '';

    this.bookService.getBooks().subscribe({

      next: (data: Book[]) => {

        console.log('BOOKS RECEIVED:', data);

        this.books = data;

        console.log('BOOKS STORED:', this.books);
        console.log('TOTAL:', this.books.length);

        this.isLoading = false;

        this.cdr.detectChanges();
      },

      error: (error) => {

        console.error('BOOK API ERROR:', error);

        this.books = [];

        this.isLoading = false;

        this.errorMessage =
          'Could not load books. Please make sure the API is running.';

        this.cdr.detectChanges();
      }

    });
  }

  edit(book: Book): void {

    console.log('Edit clicked:', book);

    window.location.href = `/form?id=${book.bookId}`;
  }

  deleteBook(bookId: number): void {

    const confirmed = confirm(
      'Are you sure you want to delete this book?'
    );

    if (!confirmed) {
      return;
    }

    this.bookService.deleteBook(bookId).subscribe({

      next: () => {

        alert('Book deleted successfully!');

        this.loadBooks();
      },

      error: (error) => {

        console.error('Error deleting book:', error);

        alert('Could not delete book.');

      }

    });
  }
}