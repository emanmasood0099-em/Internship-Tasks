USE LibraryDb_Week3;
GO

INSERT INTO Authors (FullName)
VALUES
('J.K. Rowling'),
('George Orwell'),
('Jane Austen');
GO

INSERT INTO Books (Title, AuthorId)
VALUES
('Harry Potter and the Philosopher''s Stone', 1),
('Harry Potter and the Chamber of Secrets', 1),
('1984', 2),
('Animal Farm', 2),
('Pride and Prejudice', 3),
('Sense and Sensibility', 3);
GO

INSERT INTO Categories (CategoryName)
VALUES
('Fantasy'),
('Fiction'),
('Classic'),
('Dystopian');
GO

INSERT INTO BookCategories (BookId, CategoryId)
VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 3),
(3, 4),
(4, 3),
(4, 4),
(5, 3),
(6, 3);
GO