namespace LibraryAPI.DTOs;

public class BookDto
{
    public string Title { get; set; } = string.Empty;

    public int AuthorId { get; set; }

    public int CategoryId { get; set; }
}