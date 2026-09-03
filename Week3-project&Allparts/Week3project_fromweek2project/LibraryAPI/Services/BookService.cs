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

    public async Task<List<Book>> GetAllAsync()
    {
        return await repository.GetAllAsync();
    }

    public async Task<Book?> GetByIdAsync(int id)
    {
        return await repository.GetByIdAsync(id);
    }

    public async Task<Book> AddAsync(BookDto bookDto)
    {
        var book = new Book
        {
            Title = bookDto.Title,
            AuthorId = bookDto.AuthorId
        };

        book.BookCategories.Add(new BookCategory
        {
            CategoryId = bookDto.CategoryId
        });

        return await repository.AddAsync(book);
    }

    public async Task<bool> UpdateAsync(int id, BookDto bookDto)
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

        return await repository.UpdateAsync(id, book);
    }

    public async Task<bool> DeleteAsync(int id)
    {
        return await repository.DeleteAsync(id);
    }
}