import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Book {
  bookId: number;
  title: string;
  authorId: number;
  categoryId: number;
}

@Injectable({
  providedIn: 'root'
})
export class BookService {

  private apiUrl = 'http://localhost:5032/api/Books';

  constructor(private http: HttpClient) {}

  // GET all books
  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>(this.apiUrl);
  }

  // GET book by ID
  getBookById(bookId: number): Observable<Book> {
    return this.http.get<Book>(`${this.apiUrl}/${bookId}`);
  }

  // POST add new book
  addBook(book: Omit<Book, 'bookId'>): Observable<Book> {
    return this.http.post<Book>(this.apiUrl, book);
  }

  // PUT update existing book
  updateBook(
    bookId: number,
    book: Omit<Book, 'bookId'>
  ): Observable<string> {

    return this.http.put(
      `${this.apiUrl}/${bookId}`,
      book,
      {
        responseType: 'text'
      }
    );
  }

  // DELETE book
  deleteBook(bookId: number): Observable<string> {

    return this.http.delete(
      `${this.apiUrl}/${bookId}`,
      {
        responseType: 'text'
      }
    );
  }
}