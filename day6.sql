CREATE TABLE citizens (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    city VARCHAR(100)
);

INSERT INTO citizens (name, age, city)
VALUES('Naman Sharma', 25, 'New Delhi');

INSERT INTO citizens(name, age, city)
VALUES('Deepanshu Sharma', 30, 'Mumbai');

INSERT INTO citizens(name, age, city)
VALUES('Himani Sharma', 28, 'bangalore');

SELECT * FROM citizen;
SELECT name FROM citizens;
SELECT * FROM citizens WHERE city = 'New Delhi';
UPDATE citizens SET city = 'pune' WHERE name = 'Himani Sharma';
SELECT * FROM citizens;
DELETE FROM citizens WHERE name = 'Naman Sharma';
SELECT * FROM citizens;