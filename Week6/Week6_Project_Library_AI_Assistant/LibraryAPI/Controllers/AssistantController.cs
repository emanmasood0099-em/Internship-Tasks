using LibraryAPI.Models;
using LibraryAPI.Services;
using Microsoft.AspNetCore.Mvc;
using Polly.CircuitBreaker;

namespace LibraryAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AssistantController : ControllerBase
    {
        private readonly IAiServiceClient _aiServiceClient;

        public AssistantController(IAiServiceClient aiServiceClient)
        {
            _aiServiceClient = aiServiceClient;
        }

        [HttpPost("ask")]
        public async Task<IActionResult> Ask(AskDto dto)
        {
            try
            {
                var result = await _aiServiceClient.AskAsync(dto.Question);

                return Ok(new
                {
                    answer = result
                });
            }
            catch (BrokenCircuitException)
            {
                return StatusCode(503, new
                {
                    message = "The AI assistant is temporarily unavailable. Please try again shortly."
                });
            }
            catch (HttpRequestException)
            {
                return StatusCode(503, new
                {
                    message = "The AI assistant is temporarily unavailable. Please try again shortly."
                });
            }
            catch (TaskCanceledException)
            {
                return StatusCode(503, new
                {
                    message = "The AI assistant is temporarily unavailable. Please try again shortly."
                });
            }
        }

        [HttpPost("ask/stream")]
        public async Task Stream(AskDto dto)
        {
            try
            {
                using var stream =
                    await _aiServiceClient.AskStreamAsync(dto.Question);

                Response.StatusCode = 200;
                Response.ContentType = "text/event-stream";
                Response.Headers.CacheControl = "no-cache";

                var buffer = new byte[1024];

                while (true)
                {
                    var bytesRead = await stream.ReadAsync(
                        buffer,
                        HttpContext.RequestAborted
                    );

                    if (bytesRead == 0)
                    {
                        break;
                    }

                    await Response.Body.WriteAsync(
                        buffer.AsMemory(0, bytesRead),
                        HttpContext.RequestAborted
                    );

                    await Response.Body.FlushAsync(
                        HttpContext.RequestAborted
                    );
                }
            }
            catch (BrokenCircuitException)
            {
                if (!Response.HasStarted)
                {
                    Response.StatusCode = 503;
                    await Response.WriteAsync(
                        "AI service is temporarily unavailable."
                    );
                }
            }
            catch (HttpRequestException)
            {
                if (!Response.HasStarted)
                {
                    Response.StatusCode = 503;
                    await Response.WriteAsync(
                        "AI service is temporarily unavailable."
                    );
                }
            }
            catch (TaskCanceledException)
            {
                if (!Response.HasStarted)
                {
                    Response.StatusCode = 503;
                    await Response.WriteAsync(
                        "AI service is temporarily unavailable."
                    );
                }
            }
        }
    }
}
