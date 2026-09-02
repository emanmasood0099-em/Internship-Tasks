USE LibraryDb_Week3;
GO

INSERT INTO BookCategories (BookId, CategoryId)
VALUES
(1, 1), -- Harry Potter 1 → Fantasy
(1, 2), -- Harry Potter 1 → Fiction

(2, 1), -- Harry Potter 2 → Fantasy
(2, 2), -- Harry Potter 2 → Fiction

(3, 2), -- 1984 → Fiction
(3, 4), -- 1984 → Dystopian

(4, 2), -- Animal Farm → Fiction
(4, 4), -- Animal Farm → Dystopian

(5, 2), -- Pride and Prejudice → Fiction
(5, 3), -- Pride and Prejudice → Classic

(6, 2), -- Sense and Sensibility → Fiction
(6, 3); -- Sense and Sensibility → Classic
GO

SELECT * FROM BookCategories;