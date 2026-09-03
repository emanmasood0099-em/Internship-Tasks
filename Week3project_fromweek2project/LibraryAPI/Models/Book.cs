using System.ComponentModel.DataAnnotations.Schema;

namespace LibraryAPI.Models;

public class Book
{
    public int BookId { get; set; }

    public string Title { get; set; } = string.Empty;

    public int AuthorId { get; set; }

    public Author? Author { get; set; }

    public ICollection<BookCategory> BookCategories { get; set; } = new List<BookCategory>();

    [NotMapped]
    public int? CategoryId =>
        BookCategories.FirstOrDefault()?.CategoryId;
}