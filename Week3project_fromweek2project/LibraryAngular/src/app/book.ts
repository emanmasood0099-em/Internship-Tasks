import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Book {
  id: number;
  title: string;
  author: string;
  category: string;
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
  getBookById(id: number): Observable<Book> {
    return this.http.get<Book>(`${this.apiUrl}/${id}`);
  }

  // POST add new book
  addBook(book: Omit<Book, 'id'>): Observable<Book> {
    return this.http.post<Book>(this.apiUrl, book);
  }

  // PUT update existing book
  updateBook(
    id: number,
    book: Omit<Book, 'id'>
  ): Observable<string> {

    return this.http.put(
      `${this.apiUrl}/${id}`,
      book,
      {
        responseType: 'text'
      }
    );
  }

  // DELETE book
  deleteBook(id: number): Observable<string> {

    return this.http.delete(
      `${this.apiUrl}/${id}`,
      {
        responseType: 'text'
      }
    );
  }
}