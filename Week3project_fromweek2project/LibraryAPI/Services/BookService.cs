using LibraryAPI.DTOs;
using LibraryAPI.Models;
using LibraryAPI.Repositories;

namespace LibraryAPI.Services;

public class BookService : IBookService
{
    private readonly IBookRepository repository;

    public BookService(IBookRepository repository)
    {
        this.repository = repository;
    }

    public List<Book> GetAll()
    {
        return repository.GetAll();
    }

    public Book? GetById(int id)
    {
        return repository.GetById(id);
    }

    public Book Add(BookDto bookDto)
    {
        var book = new Book
        {
            Title = bookDto.Title,
            AuthorId = bookDto.AuthorId
        };

        book.BookCategories.Add(new BookCategory
        {
            BookId = book.BookId,
            CategoryId = bookDto.CategoryId
        });

        return repository.Add(book);
    }

    public bool Update(int id, BookDto bookDto)
    {
        var book = new Book
        {
            Title = bookDto.Title,
            AuthorId = bookDto.AuthorId
        };

        book.BookCategories.Add(new BookCategory
        {
            BookId = id,
            CategoryId = bookDto.CategoryId
        });

        return repository.Update(id, book);
    }

    public bool Delete(int id)
    {
        return repository.Delete(id);
    }
}