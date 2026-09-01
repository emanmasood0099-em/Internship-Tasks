using EFCorePractice.Data;
using Microsoft.EntityFrameworkCore;

var options = new DbContextOptionsBuilder<LibraryDbContext>()
    .UseSqlServer(
        "Server=localhost;Database=EFCorePracticeDb;Trusted_Connection=True;TrustServerCertificate=True;")
    .Options;

using var context = new LibraryDbContext(options);

Console.WriteLine("EF Core Practice Project is Ready!");