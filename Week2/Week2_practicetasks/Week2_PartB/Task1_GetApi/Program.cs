var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapGet("/api/hello", () =>
{
    return "Hello from my ASP.NET Core API!";
});

app.Run();