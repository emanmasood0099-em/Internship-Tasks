using LibraryAPI.Models;

namespace LibraryAPI.Repositories;

public class BookRepository : IBookRepository
{
    private readonly List<Book> books = new()
    {
        new Book
        {
            BookId = 1,
            Title = "The Alchemist",
            AuthorId = 1
        },
        new Book
        {
            BookId = 2,
            Title = "Clean Code",
            AuthorId = 2
        },
        new Book
        {
            BookId = 3,
            Title = "Harry Potter",
            AuthorId = 3
        }
    };

    public List<Book> GetAll()
    {
        return books;
    }

    public Book? GetById(int id)
    {
        return books.FirstOrDefault(book => book.BookId == id);
    }

    public Book Add(Book book)
    {
        int newId = books.Count == 0
            ? 1
            : books.Max(book => book.BookId) + 1;

        book.BookId = newId;
        books.Add(book);

        return book;
    }

    public bool Update(int id, Book book)
    {
        var existingBook = books.FirstOrDefault(b => b.BookId == id);

        if (existingBook == null)
        {
            return false;
        }

        existingBook.Title = book.Title;
        existingBook.AuthorId = book.AuthorId;
        existingBook.BookCategories = book.BookCategories;

        return true;
    }

    public bool Delete(int id)
    {
        var book = books.FirstOrDefault(b => b.BookId == id);

        if (book == null)
        {
            return false;
        }

        books.Remove(book);

        return true;
    }
}