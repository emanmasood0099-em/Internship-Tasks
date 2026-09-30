using System.Net.Http.Json;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddCors(options =>
{
    options.AddPolicy("Angular", policy =>
    {
        policy
            .WithOrigins("http://localhost:4200")
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

builder.Services.AddHttpClient("AIService", client =>
{
    client.BaseAddress = new Uri("http://127.0.0.1:8000");
    client.Timeout = Timeout.InfiniteTimeSpan;
});

var app = builder.Build();

app.UseCors("Angular");

app.MapPost("/api/assistant/ask/stream", async (
    AskRequest request,
    IHttpClientFactory httpClientFactory,
    HttpContext context) =>
{
    context.Response.ContentType = "text/event-stream";
    context.Response.Headers.CacheControl = "no-cache";

    try
    {
        var client = httpClientFactory.CreateClient("AIService");

        using var upstreamRequest = new HttpRequestMessage(
            HttpMethod.Post,
            "/ask/stream"
        );

        upstreamRequest.Content = JsonContent.Create(new
        {
            question = request.Question
        });

        using var upstreamResponse = await client.SendAsync(
            upstreamRequest,
            HttpCompletionOption.ResponseHeadersRead,
            context.RequestAborted
        );

        upstreamResponse.EnsureSuccessStatusCode();

        await using var stream =
            await upstreamResponse.Content.ReadAsStreamAsync(
                context.RequestAborted
            );

        using var reader = new StreamReader(stream);

        while (!reader.EndOfStream)
        {
            var line = await reader.ReadLineAsync(
                context.RequestAborted
            );

            if (string.IsNullOrEmpty(line))
                continue;

            await context.Response.WriteAsync(
                line + "\n\n",
                context.RequestAborted
            );

            await context.Response.Body.FlushAsync(
                context.RequestAborted
            );
        }
    }
    catch (OperationCanceledException)
        when (context.RequestAborted.IsCancellationRequested)
    {
        Console.WriteLine(
            "CANCELLATION TEST: Client disconnected. Upstream AI streaming request was cancelled."
        );
    }
});

app.Run();

public record AskRequest(string Question);