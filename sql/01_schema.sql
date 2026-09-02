CREATE DATABASE LibraryDb_Week3;
GO

USE LibraryDb_Week3;
GO

CREATE TABLE Authors
(
    AuthorId INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(100) NOT NULL
);
GO

CREATE TABLE Categories
(
    CategoryId INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL
);
GO

CREATE TABLE Books
(
    BookId INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(200) NOT NULL,
    AuthorId INT NOT NULL,

    CONSTRAINT FK_Books_Authors
        FOREIGN KEY (AuthorId)
        REFERENCES Authors(AuthorId)
);
GO

CREATE TABLE BookCategories
(
    BookId INT NOT NULL,
    CategoryId INT NOT NULL,

    CONSTRAINT PK_BookCategories
        PRIMARY KEY (BookId, CategoryId),

    CONSTRAINT FK_BookCategories_Books
        FOREIGN KEY (BookId)
        REFERENCES Books(BookId),

    CONSTRAINT FK_BookCategories_Categories
        FOREIGN KEY (CategoryId)
        REFERENCES Categories(CategoryId)
);
GO