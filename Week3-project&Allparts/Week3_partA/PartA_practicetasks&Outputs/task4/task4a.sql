USE LibraryDb_Week3;
GO

CREATE TABLE Categories
(
    CategoryId INT PRIMARY KEY IDENTITY(1,1),
    CategoryName NVARCHAR(100) NOT NULL
);
GO