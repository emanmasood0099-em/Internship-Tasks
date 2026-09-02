using LibraryAPI.DTOs;
using LibraryAPI.Models;

namespace LibraryAPI.Services;

public interface IBookService
{
    List<Book> GetAll();

    Book? GetById(int id);

    Book Add(BookDto bookDto);

    bool Update(int id, BookDto bookDto);

    bool Delete(int id);
}