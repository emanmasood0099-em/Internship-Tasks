var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

// 200 OK
app.MapGet("/api/status/ok", () =>
{
    return Results.Ok("Request successful - 200 OK");
});

// 201 Created
app.MapPost("/api/status/create", () =>
{
    return Results.Created("/api/status/create", "Data created successfully - 201 Created");
});

// 400 Bad Request
app.MapGet("/api/status/check/{number}", (int number) =>
{
    if (number < 0)
    {
        return Results.BadRequest("Number cannot be negative - 400 Bad Request");
    }

    return Results.Ok("Number is valid - 200 OK");
});

// 404 Not Found
app.MapGet("/api/status/student/{id}", (int id) =>
{
    if (id != 1)
    {
        return Results.NotFound("Student not found - 404 Not Found");
    }

    return Results.Ok("Student found - 200 OK");
});

app.Run();