USE LibraryDb_Week3;
GO

SELECT
    b.BookId,
    b.Title,
    a.FullName AS Author
FROM Books b
JOIN Authors a
    ON b.AuthorId = a.AuthorId
ORDER BY a.FullName;
GO

SELECT
    b.Title,
    c.CategoryName
FROM BookCategories bc
JOIN Books b
    ON bc.BookId = b.BookId
JOIN Categories c
    ON bc.CategoryId = c.CategoryId
WHERE b.BookId = 1;
GO

DELETE FROM Authors
WHERE AuthorId = 1;
GO