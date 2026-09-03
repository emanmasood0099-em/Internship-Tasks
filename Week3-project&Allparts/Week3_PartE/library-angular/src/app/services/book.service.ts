import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Book {
  id: number;
  title: string;
  author: string;
}

export interface CreateBook {
  title: string;
  author: string;
}

@Injectable({
  providedIn: 'root'
})
export class BookService {

  private apiUrl = `${environment.apiUrl}/api/books`;

  constructor(private http: HttpClient) {}

  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>(this.apiUrl);
  }

  addBook(book: CreateBook): Observable<Book> {
    return this.http.post<Book>(this.apiUrl, book);
  }
}