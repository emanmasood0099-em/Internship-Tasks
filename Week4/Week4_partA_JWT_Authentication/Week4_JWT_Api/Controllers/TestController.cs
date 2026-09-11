using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Week4_JWT_Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TestController : ControllerBase
{
    [HttpGet("protected")]
    [Authorize]
    public IActionResult Protected()
    {
        return Ok("You accessed the protected endpoint successfully.");
    }
}