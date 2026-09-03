using LibraryAPI.Data;
using LibraryAPI.Models;
using Microsoft.EntityFrameworkCore;

namespace LibraryAPI.Repositories;

public class BookRepository : IBookRepository
{
    private readonly LibraryDbContext context;

    public BookRepository(LibraryDbContext context)
    {
        this.context = context;
    }

    public async Task<List<Book>> GetAllAsync()
    {
        return await context.Books
            .Include(b => b.BookCategories)
            .ToListAsync();
    }

    public async Task<Book?> GetByIdAsync(int id)
    {
        return await context.Books
            .Include(b => b.BookCategories)
            .FirstOrDefaultAsync(b => b.BookId == id);
    }

    public async Task<Book> AddAsync(Book book)
    {
        context.Books.Add(book);
        await context.SaveChangesAsync();

        return book;
    }

    public async Task<bool> UpdateAsync(int id, Book book)
    {
        var existingBook = await context.Books
            .Include(b => b.BookCategories)
            .FirstOrDefaultAsync(b => b.BookId == id);

        if (existingBook == null)
        {
            return false;
        }

        existingBook.Title = book.Title;
        existingBook.AuthorId = book.AuthorId;

        context.BookCategories.RemoveRange(existingBook.BookCategories);

        foreach (var bookCategory in book.BookCategories)
        {
            existingBook.BookCategories.Add(new BookCategory
            {
                BookId = id,
                CategoryId = bookCategory.CategoryId
            });
        }

        await context.SaveChangesAsync();

        return true;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var book = await context.Books
            .FirstOrDefaultAsync(b => b.BookId == id);

        if (book == null)
        {
            return false;
        }

        context.Books.Remove(book);
        await context.SaveChangesAsync();

        return true;
    }
}