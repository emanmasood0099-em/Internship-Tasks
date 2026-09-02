using LibraryAPI.Models;

namespace LibraryAPI.Repositories;

public interface IBookRepository
{
    List<Book> GetAll();

    Book? GetById(int id);

    Book Add(Book book);

    bool Update(int id, Book book);

    bool Delete(int id);
}