var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapGet("/api/greet/{name}", (string name) =>
{
    return "Hello, " + name + "!";
});

app.Run();