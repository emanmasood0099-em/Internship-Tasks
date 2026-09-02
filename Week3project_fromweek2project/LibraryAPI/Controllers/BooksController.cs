using LibraryAPI.DTOs;
using LibraryAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace LibraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class BooksController : ControllerBase
{
    private readonly IBookService service;

    public BooksController(IBookService service)
    {
        this.service = service;
    }

    // GET: api/books
    [HttpGet]
    public IActionResult GetAll()
    {
        var books = service.GetAll();

        return Ok(books);
    }

    // GET: api/books/1
    [HttpGet("{id}")]
    public IActionResult GetById(int id)
    {
        var book = service.GetById(id);

        if (book == null)
        {
            return NotFound("Book not found - 404 Not Found");
        }

        return Ok(book);
    }

    // POST: api/books
    [HttpPost]
    public IActionResult Create(BookDto bookDto)
    {
        var book = service.Add(bookDto);

        return CreatedAtAction(
            nameof(GetById),
            new { id = book.BookId },
            book
        );
    }

    // PUT: api/books/1
    [HttpPut("{id}")]
    public IActionResult Update(int id, BookDto bookDto)
    {
        var updated = service.Update(id, bookDto);

        if (!updated)
        {
            return NotFound("Book not found - 404 Not Found");
        }

        return Ok("Book updated successfully - 200 OK");
    }

    // DELETE: api/books/1
    [HttpDelete("{id}")]
    public IActionResult Delete(int id)
    {
        var deleted = service.Delete(id);

        if (!deleted)
        {
            return NotFound("Book not found - 404 Not Found");
        }

        return Ok("Book deleted successfully - 200 OK");
    }
}