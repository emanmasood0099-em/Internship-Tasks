USE LibraryDb_Week3;
GO

SELECT
    Books.Title AS Book,
    Categories.CategoryName AS Category
FROM Books
INNER JOIN BookCategories
    ON Books.BookId = BookCategories.BookId
INNER JOIN Categories
    ON BookCategories.CategoryId = Categories.CategoryId
WHERE Books.BookId = 1;