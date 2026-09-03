import {
  Component,
  OnInit
} from '@angular/core';

import {
  ReactiveFormsModule,
  FormGroup,
  FormControl,
  Validators
} from '@angular/forms';

import { ActivatedRoute, Router } from '@angular/router';

import { BookService } from '../book';

@Component({
  selector: 'app-book-form',
  imports: [ReactiveFormsModule],
  templateUrl: './book-form.html',
  styleUrl: './book-form.css'
})
export class BookForm implements OnInit {

  isEditMode = false;

  editBookId: number | null = null;

  bookForm = new FormGroup({

    title: new FormControl('', [
      Validators.required,
      Validators.minLength(2)
    ]),

    authorId: new FormControl<number | null>(null, [
      Validators.required
    ]),

    categoryId: new FormControl<number | null>(null, [
      Validators.required
    ])

  });

  constructor(
    private bookService: BookService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {

    const id = this.route.snapshot.queryParamMap.get('id');

    if (id) {

      this.isEditMode = true;

      this.editBookId = Number(id);

      console.log('Editing book ID:', this.editBookId);

      this.loadBook(this.editBookId);
    }
  }

  loadBook(id: number): void {

    this.bookService.getBookById(id).subscribe({

      next: (book) => {

        console.log('Book loaded for editing:', book);

        this.bookForm.patchValue({

          title: book.title,

          authorId: book.authorId,

          categoryId: book.categoryId

        });

      },

      error: (error) => {

        console.error('Error loading book:', error);

        alert('Could not load book.');
      }

    });
  }

  submitForm(): void {

    if (this.bookForm.invalid) {

      this.bookForm.markAllAsTouched();

      return;
    }

    const book = {

      title: this.bookForm.value.title!,

      authorId: this.bookForm.value.authorId!,

      categoryId: this.bookForm.value.categoryId!

    };

    // UPDATE

    if (this.isEditMode && this.editBookId !== null) {

      this.bookService
        .updateBook(this.editBookId, book)
        .subscribe({

          next: (response) => {

            console.log(
              'Book updated successfully:',
              response
            );

            alert('Book updated successfully!');

            this.bookForm.reset();

            this.isEditMode = false;

            this.editBookId = null;

            this.router.navigate(['/books']);

          },

          error: (error) => {

            console.error(
              'Error updating book:',
              error
            );

            alert('Could not update book.');
          }

        });

      return;
    }

    // ADD

    this.bookService.addBook(book).subscribe({

      next: (response) => {

        console.log(
          'Book added successfully:',
          response
        );

        alert('Book added successfully!');

        this.bookForm.reset();

        this.router.navigate(['/books']);

      },

      error: (error) => {

        console.error(
          'Error adding book:',
          error
        );

        alert('Could not add book.');
      }

    });
  }

  cancelEdit(): void {

    this.bookForm.reset();

    this.isEditMode = false;

    this.editBookId = null;

    this.router.navigate(['/books']);

  }
}