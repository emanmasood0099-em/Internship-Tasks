using LibraryAPI.Data;
using LibraryAPI.DTOs;
using LibraryAPI.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace LibraryAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly LibraryDbContext _context;
    private readonly IConfiguration _configuration;
    private readonly PasswordHasher<User> _passwordHasher;

    public AuthController(
        LibraryDbContext context,
        IConfiguration configuration)
    {
        _context = context;
        _configuration = configuration;
        _passwordHasher = new PasswordHasher<User>();
    }

    // POST: api/auth/register
    [HttpPost("register")]
    public IActionResult Register(RegisterDto registerDto)
    {
        var existingUser = _context.Users
            .FirstOrDefault(u => u.Username == registerDto.Username);

        if (existingUser != null)
        {
            return BadRequest(new
            {
                message = "Username already exists."
            });
        }

        var user = new User
        {
            Username = registerDto.Username,
            Role = registerDto.Role
        };

        user.PasswordHash = _passwordHasher.HashPassword(
            user,
            registerDto.Password);

        _context.Users.Add(user);
        _context.SaveChanges();

        return Ok(new
        {
            message = "User registered successfully."
        });
    }

    // POST: api/auth/login
    [HttpPost("login")]
    public IActionResult Login(LoginDto loginDto)
    {
        var user = _context.Users
            .FirstOrDefault(u => u.Username == loginDto.Username);

        if (user == null)
        {
            return Unauthorized(new
            {
                message = "Invalid username or password."
            });
        }

        var result = _passwordHasher.VerifyHashedPassword(
            user,
            user.PasswordHash,
            loginDto.Password);

        if (result == PasswordVerificationResult.Failed)
        {
            return Unauthorized(new
            {
                message = "Invalid username or password."
            });
        }

        var token = GenerateJwtToken(user);

        return Ok(new
        {
            token = token,
            username = user.Username,
            role = user.Role
        });
    }

    private string GenerateJwtToken(User user)
    {
        var jwtSettings = _configuration.GetSection("Jwt");

        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(jwtSettings["Key"]!));

        var credentials = new SigningCredentials(
            key,
            SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(ClaimTypes.Name, user.Username),
            new Claim(ClaimTypes.Role, user.Role)
        };

        var token = new JwtSecurityToken(
            issuer: jwtSettings["Issuer"],
            audience: jwtSettings["Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(
                double.Parse(jwtSettings["ExpiryMinutes"]!)),
            signingCredentials: credentials);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}