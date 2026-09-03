using LibraryApi.Models;
using LibraryApi.Repositories;
using Microsoft.AspNetCore.Mvc;

namespace LibraryApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class BooksController : ControllerBase
{
    private readonly IBookRepository _repository;

    public BooksController(IBookRepository repository)
    {
        _repository = repository;
    }

    [HttpGet]
    public async Task<ActionResult<List<Book>>> GetAll()
    {
        var books = await _repository.GetAllAsync();
        return Ok(books);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Book>> GetById(int id)
    {
        var book = await _repository.GetByIdAsync(id);

        if (book == null)
            return NotFound(new { message = "Book not found." });

        return Ok(book);
    }

    [HttpPost]
    public async Task<ActionResult<Book>> Create(Book book)
    {
        try
        {
            var createdBook = await _repository.AddAsync(book);

            return CreatedAtAction(
                nameof(GetById),
                new { id = createdBook.BookId },
                createdBook);
        }
        catch (Exception)
        {
            return StatusCode(500, new
            {
                message = "An error occurred while saving the book."
            });
        }
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        try
        {
            var deleted = await _repository.DeleteAsync(id);

            if (!deleted)
                return NotFound(new { message = "Book not found." });

            return NoContent();
        }
        catch (Exception)
        {
            return StatusCode(500, new
            {
                message = "An error occurred while deleting the book."
            });
        }
    }
}