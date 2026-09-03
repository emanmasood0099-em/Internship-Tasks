USE LibraryDb_Week3;
GO

SELECT
    Books.Title AS Book,
    Authors.FullName AS AuthorS
FROM Books
INNER JOIN Authors
    ON Books.AuthorId = Authors.AuthorId
ORDER BY Authors.FullName;