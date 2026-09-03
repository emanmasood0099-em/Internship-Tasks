using LibraryAPI.DTOs;
using LibraryAPI.Models;

namespace LibraryAPI.Services;

public interface IBookService
{
    Task<List<Book>> GetAllAsync();

    Task<Book?> GetByIdAsync(int id);

    Task<Book> AddAsync(BookDto bookDto);

    Task<bool> UpdateAsync(int id, BookDto bookDto);

    Task<bool> DeleteAsync(int id);
}