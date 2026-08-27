var builder = WebApplication.CreateBuilder(args);

// OpenAPI
builder.Services.AddOpenApi();

// Swagger
builder.Services.AddSwaggerGen();

var app = builder.Build();

// OpenAPI + Swagger UI
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.UseSwagger();
    app.UseSwaggerUI();
}

// 200 OK
app.MapGet("/api/status/ok", () =>
{
    return Results.Ok("Request successful - 200 OK");
})
.Produces<string>(StatusCodes.Status200OK);

// 201 Created

app.MapPost("/api/status/create", () =>
{
    return Results.Created(
        "/api/status/create",
        "Data created successfully - 201 Created"
    );
})
.Produces<string>(StatusCodes.Status201Created);

// 400 Bad Request
app.MapGet("/api/status/check/{number}", (int number) =>
{
    if (number < 0)
    {
        return Results.BadRequest(
            "Number cannot be negative - 400 Bad Request"
        );
    }

    return Results.Ok("Number is valid - 200 OK");
})
.Produces<string>(StatusCodes.Status200OK)
.Produces<string>(StatusCodes.Status400BadRequest);

// 404 Not Found
app.MapGet("/api/status/student/{id}", (int id) =>
{
    if (id != 1)
    {
        return Results.NotFound(
            "Student not found - 404 Not Found"
        );
    }

    return Results.Ok("Student found - 200 OK");
})
.Produces<string>(StatusCodes.Status200OK)
.Produces<string>(StatusCodes.Status404NotFound);

app.Run();