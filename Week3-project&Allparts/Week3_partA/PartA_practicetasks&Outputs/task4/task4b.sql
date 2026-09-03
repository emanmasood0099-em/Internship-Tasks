USE LibraryDb_Week3;
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