using LibraryAPI.Models;

namespace LibraryAPI.Repositories;

public class BookRepository : IBookRepository
{
    private readonly List<Book> books = new()
    {
        new Book
        {
            Id = 1,
            Title = "The Alchemist",
            Author = "Paulo Coelho",
            Category = "Fiction"
        },
        new Book
        {
            Id = 2,
            Title = "Clean Code",
            Author = "Robert C. Martin",
            Category = "Programming"
        },
        new Book
        {
            Id = 3,
            Title = "Harry Potter",
            Author = "J.K. Rowling",
            Category = "Fantasy"
        }
    };

    public List<Book> GetAll()
    {
        return books;
    }

    public Book? GetById(int id)
    {
        return books.FirstOrDefault(book => book.Id == id);
    }

    public Book Add(Book book)
    {
        int newId = books.Count == 0
            ? 1
            : books.Max(book => book.Id) + 1;

        book.Id = newId;
        books.Add(book);

        return book;
    }

    public bool Update(int id, Book book)
    {
        Console.WriteLine($"UPDATE REQUEST: ID = {id}");
        Console.WriteLine($"New Title = {book.Title}");
        Console.WriteLine($"New Author = {book.Author}");
        Console.WriteLine($"New Category = {book.Category}");

        var existingBook = books.FirstOrDefault(b => b.Id == id);

        if (existingBook == null)
        {
            Console.WriteLine("BOOK NOT FOUND");
            return false;
        }

        existingBook.Title = book.Title;
        existingBook.Author = book.Author;
        existingBook.Category = book.Category;

        Console.WriteLine($"BOOK UPDATED: {existingBook.Title}");

        return true;
    }

    public bool Delete(int id)
    {
        var book = books.FirstOrDefault(b => b.Id == id);

        if (book == null)
        {
            return false;
        }

        books.Remove(book);

        return true;
    }
}