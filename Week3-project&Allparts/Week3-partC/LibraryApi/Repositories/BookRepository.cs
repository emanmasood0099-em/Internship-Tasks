using LibraryApi.Data;
using LibraryApi.Models;
using Microsoft.EntityFrameworkCore;

namespace LibraryApi.Repositories;

public class BookRepository : IBookRepository
{
    private readonly LibraryDbContext _context;

    public BookRepository(LibraryDbContext context)
    {
        _context = context;
    }

    public async Task<List<Book>> GetAllAsync()
    {
        return await _context.Books.ToListAsync();
    }

    public async Task<Book?> GetByIdAsync(int id)
    {
        return await _context.Books.FindAsync(id);
    }

    public async Task<Book> AddAsync(Book book)
    {
        try
        {
            _context.Books.Add(book);
            await _context.SaveChangesAsync();

            return book;
        }
        catch (Exception)
        {
            throw new Exception("Unable to save the book to the database.");
        }
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var book = await _context.Books.FindAsync(id);

        if (book == null)
            return false;

        _context.Books.Remove(book);
        await _context.SaveChangesAsync();

        return true;
    }
}