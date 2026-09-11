using Microsoft.EntityFrameworkCore;
using Week4_JWT_Api.Models;

namespace Week4_JWT_Api.Data;

public class AuthDbContext : DbContext
{
    public AuthDbContext(DbContextOptions<AuthDbContext> options)
        : base(options)
    {
    }

    public DbSet<User> Users { get; set; }
}