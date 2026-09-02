var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenApi();
builder.Services.AddCors(options =>
{
    options.AddPolicy("AngularPolicy", policy =>
    {
        policy
            .WithOrigins("http://localhost:4200")
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

app.UseCors("AngularPolicy");

var books = new List<Book>
{
    new Book { Id = 1, Title = "The Alchemist", Author = "Paulo Coelho" },
    new Book { Id = 2, Title = "Atomic Habits", Author = "James Clear" }
};

app.MapGet("/api/books", async () =>
{
    await Task.Delay(3000);
    return Results.Ok(books);
});

app.MapPost("/api/books", (CreateBook request) =>
{
    var book = new Book
    {
        Id = books.Count + 1,
        Title = request.Title,
        Author = request.Author
    };

    books.Add(book);

    return Results.Created($"/api/books/{book.Id}", book);
});

app.Run();

public class Book
{
    public int Id { get; set; }
    public string Title { get; set; } = "";
    public string Author { get; set; } = "";
}

public class CreateBook
{
    public string Title { get; set; } = "";
    public string Author { get; set; } = "";
}