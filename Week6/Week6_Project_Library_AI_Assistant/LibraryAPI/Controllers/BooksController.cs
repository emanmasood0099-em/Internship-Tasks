using LibraryAPI.Data;
using LibraryAPI.DTOs;
using LibraryAPI.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace LibraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class BooksController : ControllerBase
{
    private readonly IBookService service;
    private readonly LibraryDbContext context;

    public BooksController(
        IBookService service,
        LibraryDbContext context)
    {
        this.service = service;
        this.context = context;
    }

    // GET: api/books
    // Public endpoint
    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var books = await service.GetAllAsync();

        return Ok(books);
    }

    // GET: api/books/1
    // Public endpoint
    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
        var book = await service.GetByIdAsync(id);

        if (book == null)
        {
            return NotFound("Book not found - 404 Not Found");
        }

        return Ok(book);
    }

    // GET: api/books/1/availability
    // Public endpoint - Part D Tool Calling
    [HttpGet("{id}/availability")]
    public async Task<IActionResult> CheckAvailability(int id)
    {
        var book = await context.Books
            .AsNoTracking()
            .FirstOrDefaultAsync(b => b.BookId == id);

        if (book == null)
        {
            return NotFound("Book not found - 404 Not Found");
        }

        return Ok(new
        {
            bookId = book.BookId,
            title = book.Title,
            isAvailable = book.IsAvailable
        });
    }

    // POST: api/books
    // Logged-in users only
    [Authorize]
    [HttpPost]
    public async Task<IActionResult> Create(BookDto bookDto)
    {
        var book = await service.AddAsync(bookDto);

        return CreatedAtAction(
            nameof(GetById),
            new { id = book.BookId },
            book
        );
    }

    // PUT: api/books/1
    // Logged-in users only
    [Authorize]
    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, BookDto bookDto)
    {
        var updated = await service.UpdateAsync(id, bookDto);

        if (!updated)
        {
            return NotFound("Book not found - 404 Not Found");
        }

        return Ok("Book updated successfully - 200 OK");
    }

    // DELETE: api/books/1
    // Admin users only
    [Authorize(Roles = "Admin")]
    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var deleted = await service.DeleteAsync(id);

        if (!deleted)
        {
            return NotFound("Book not found - 404 Not Found");
        }

        return Ok("Book deleted successfully - 200 OK");
    }
}
