# Internship Tasks

## Week 3 — SQL Server + Entity Framework Core + API/Angular Integration

This repository contains the Week 3 implementation completed during the internship.

---

## Project Overview

The Week 3 project demonstrates the integration of:

- SQL Server
- Entity Framework Core
- ASP.NET Core Web API
- Angular
- Repository Pattern
- Service Layer
- HTTP communication
- Basic authentication foundation

Application flow:

Angular
↓
ASP.NET Core Web API
↓
Service Layer
↓
Repository Layer
↓
Entity Framework Core
↓
SQL Server

---

## Database

Database used:

`LibraryDb_Week3`

### Main Tables

- Authors
- Categories
- Books
- BookCategories
- Users

### Relationships

- One Author can have many Books.
- Books and Categories have a many-to-many relationship through `BookCategories`.
- `Books.AuthorId` is a foreign key referencing `Authors.AuthorId`.
- `BookCategories.BookId` references `Books.BookId`.
- `BookCategories.CategoryId` references `Categories.CategoryId`.

---

## Entity Framework Core

EF Core is used as the data access layer.

### DbContext

`LibraryDbContext` manages the database entities:

- `Books`
- `Authors`
- `Categories`
- `BookCategories`
- `Users`

### Migrations

A migration named `AddUser` was created to add the `Users` table.

```text
20260903014116_AddUser