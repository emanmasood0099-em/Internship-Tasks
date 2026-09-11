using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Week4_JWT_Api.Data;
using Week4_JWT_Api.Models;

namespace Week4_JWT_Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly AuthDbContext _context;
    private readonly IConfiguration _configuration;

    public AuthController(
        AuthDbContext context,
        IConfiguration configuration)
    {
        _context = context;
        _configuration = configuration;
    }

    // POST: api/auth/register
    [HttpPost("register")]
    public async Task<IActionResult> Register(User user)
    {
        var existingUser = await _context.Users
            .FirstOrDefaultAsync(u => u.Username == user.Username);

        if (existingUser != null)
        {
            return BadRequest("Username already exists.");
        }

        user.PasswordHash =
            BCrypt.Net.BCrypt.HashPassword(user.PasswordHash);

        user.Role = "User";

        _context.Users.Add(user);
        await _context.SaveChangesAsync();

        return Ok("User registered successfully.");
    }

    // POST: api/auth/login
    [HttpPost("login")]
    public async Task<IActionResult> Login(User loginUser)
    {
        var user = await _context.Users
            .FirstOrDefaultAsync(u => u.Username == loginUser.Username);

        if (user == null)
        {
            return Unauthorized("Invalid username or password.");
        }

        bool passwordValid =
            BCrypt.Net.BCrypt.Verify(
                loginUser.PasswordHash,
                user.PasswordHash);

        if (!passwordValid)
        {
            return Unauthorized("Invalid username or password.");
        }

        var token = GenerateJwtToken(user);

        return Ok(new
        {
            token = token
        });
    }

    private string GenerateJwtToken(User user)
    {
        var jwtKey = _configuration["Jwt:Key"]
            ?? throw new InvalidOperationException(
                "JWT Key is missing.");

        var jwtIssuer = _configuration["Jwt:Issuer"]
            ?? throw new InvalidOperationException(
                "JWT Issuer is missing.");

        var jwtAudience = _configuration["Jwt:Audience"]
            ?? throw new InvalidOperationException(
                "JWT Audience is missing.");

        var expiryMinutes = int.Parse(
            _configuration["Jwt:ExpiryMinutes"] ?? "60");

        var claims = new[]
        {
            new Claim(ClaimTypes.Name, user.Username),
            new Claim(ClaimTypes.Role, user.Role)
        };

        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(jwtKey))
        {
            KeyId = "Week4JWTKey"
        };

        var credentials = new SigningCredentials(
            key,
            SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: jwtIssuer,
            audience: jwtAudience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(expiryMinutes),
            signingCredentials: credentials);

        return new JwtSecurityTokenHandler()
            .WriteToken(token);
    }
}