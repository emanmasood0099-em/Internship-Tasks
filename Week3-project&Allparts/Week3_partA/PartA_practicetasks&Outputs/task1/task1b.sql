-- Week 3 - Task 1
-- Create Authors and Books tables

USE LibraryDb_Week3;
GO

CREATE TABLE Authors
(
    AuthorId INT PRIMARY KEY IDENTITY(1,1),
    FullName NVARCHAR(100) NOT NULL
);
GO

CREATE TABLE Books
(
    BookId INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(200) NOT NULL,
    AuthorId INT NOT NULL,

    CONSTRAINT FK_Books_Authors
        FOREIGN KEY (AuthorId)
        REFERENCES Authors(AuthorId)
);
GO