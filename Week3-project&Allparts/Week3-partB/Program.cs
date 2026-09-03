/*

part b - task2 

using EFCorePractice.Data;
using EFCorePractice.Models;
using Microsoft.EntityFrameworkCore;

var options = new DbContextOptionsBuilder<LibraryDbContext>()
    .UseSqlServer(
        "Server=localhost;Database=EFCorePracticeDb;Trusted_Connection=True;TrustServerCertificate=True;")
    .Options;

using var context = new LibraryDbContext(options);

// INSERT
var book = new Book
{
    Title = "The Alchemist"
};

context.Books.Add(book);
await context.SaveChangesAsync();

Console.WriteLine("Book inserted successfully!");

// RETRIEVE
var books = await context.Books.ToListAsync();

Console.WriteLine("\nBooks in database:");

foreach (var b in books)
{
    Console.WriteLine($"BookId: {b.BookId}, Title: {b.Title}");
}
*/

//part b - task 3

/*
using EFCorePractice.Data;
using EFCorePractice.Models;
using Microsoft.EntityFrameworkCore;

var options = new DbContextOptionsBuilder<LibraryDbContext>()
    .UseSqlServer(
        "Server=localhost;Database=EFCorePracticeDb;Trusted_Connection=True;TrustServerCertificate=True;")
    .Options;

using var context = new LibraryDbContext(options);

// INSERT a second book for the delete operation
var secondBook = new Book
{
    Title = "Clean Code"
};

context.Books.Add(secondBook);
await context.SaveChangesAsync();

Console.WriteLine("Second book inserted successfully!");

// UPDATE Book 1
var bookToUpdate = await context.Books
    .FirstOrDefaultAsync(b => b.BookId == 1);

if (bookToUpdate != null)
{
    bookToUpdate.Title = "The Alchemist - Updated";

    await context.SaveChangesAsync();

    Console.WriteLine("Book 1 updated successfully!");
}

// DELETE Book 2
var bookToDelete = await context.Books
    .FirstOrDefaultAsync(b => b.BookId == secondBook.BookId);

if (bookToDelete != null)
{
    context.Books.Remove(bookToDelete);

    await context.SaveChangesAsync();

    Console.WriteLine("Book 2 deleted successfully!");
}

// RETRIEVE remaining books
var books = await context.Books.ToListAsync();

Console.WriteLine("\nBooks remaining in database:");

foreach (var book in books)
{
    Console.WriteLine($"BookId: {book.BookId}, Title: {book.Title}");
}

*/

//  part b - task 4

using EFCorePractice.Data;
using Microsoft.EntityFrameworkCore;

var options = new DbContextOptionsBuilder<LibraryDbContext>()
    .UseSqlServer(
        "Server=localhost;Database=EFCorePracticeDb;Trusted_Connection=True;TrustServerCertificate=True;")
    .Options;

using var context = new LibraryDbContext(options);

// FILTERED LINQ QUERY
var filteredBooks = await context.Books
    .Where(b => b.Title.Contains("Alchemist"))
    .ToListAsync();

Console.WriteLine("Filtered books:");

foreach (var book in filteredBooks)
{
    Console.WriteLine($"BookId: {book.BookId}, Title: {book.Title}");
}