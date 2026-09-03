using LibraryAPI.DTOs;
using Microsoft.AspNetCore.Mvc;

namespace LibraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    // POST: api/auth/login
    [HttpPost("login")]
    public IActionResult Login(LoginDto loginDto)
    {
        return Ok(new
        {
            message = "Login endpoint skeleton is working.",
            username = loginDto.Username
        });
    }
}