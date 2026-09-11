using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.Text;
using Week4_JWT_Api.Data;

var builder = WebApplication.CreateBuilder(args);

// Add Entity Framework Core with SQL Server
builder.Services.AddDbContext<AuthDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString(
            "DefaultConnection")));

// Add JWT Authentication
var jwtKey = builder.Configuration["Jwt:Key"]
    ?? throw new InvalidOperationException(
        "JWT Key is missing.");

var jwtIssuer = builder.Configuration["Jwt:Issuer"]
    ?? throw new InvalidOperationException(
        "JWT Issuer is missing.");

var jwtAudience = builder.Configuration["Jwt:Audience"]
    ?? throw new InvalidOperationException(
        "JWT Audience is missing.");

builder.Services.AddAuthentication(
    JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        // Show JWT validation errors in terminal
        options.Events = new JwtBearerEvents
        {
            OnAuthenticationFailed = context =>
            {
                Console.WriteLine(
                    "JWT ERROR: " +
                    context.Exception.Message);

                return Task.CompletedTask;
            }
        };

        options.TokenValidationParameters =
            new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidateAudience = true,
                ValidateLifetime = true,
                ValidateIssuerSigningKey = true,

                ValidIssuer = jwtIssuer,
                ValidAudience = jwtAudience,

                IssuerSigningKey =
                    new SymmetricSecurityKey(
                        Encoding.UTF8.GetBytes(jwtKey))
                    {
                        KeyId = "Week4JWTKey"
                    }
            };
    });

// Add Authorization
builder.Services.AddAuthorization();

// Add Controllers
builder.Services.AddControllers();

// Add Swagger
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSwaggerGen(options =>
{
    options.AddSecurityDefinition(
        "Bearer",
        new Microsoft.OpenApi.OpenApiSecurityScheme
        {
            Name = "Authorization",
            Type = Microsoft.OpenApi.SecuritySchemeType.Http,
            Scheme = "bearer",
            BearerFormat = "JWT",
            In = Microsoft.OpenApi.ParameterLocation.Header,
            Description = "Enter your JWT token."
        });

    options.AddSecurityRequirement(document =>
        new Microsoft.OpenApi.OpenApiSecurityRequirement
        {
            {
                new Microsoft.OpenApi.OpenApiSecuritySchemeReference(
                    "Bearer",
                    document),
                new List<string>()
            }
        });
});

var app = builder.Build();

// Swagger
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Authentication MUST come before Authorization
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();