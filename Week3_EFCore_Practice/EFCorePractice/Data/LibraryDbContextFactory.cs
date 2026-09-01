using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace EFCorePractice.Data;

public class LibraryDbContextFactory : IDesignTimeDbContextFactory<LibraryDbContext>
{
    public LibraryDbContext CreateDbContext(string[] args)
    {
        var optionsBuilder = new DbContextOptionsBuilder<LibraryDbContext>();

        optionsBuilder.UseSqlServer(
            "Server=localhost;Database=EFCorePracticeDb;Trusted_Connection=True;TrustServerCertificate=True;");

        return new LibraryDbContext(optionsBuilder.Options);
    }
}