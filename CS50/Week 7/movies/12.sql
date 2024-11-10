SELECT title
FROM movies
WHERE id IN
(
    SELECT s.movie_id
    FROM stars AS s
    WHERE person_id IN
        (
            SELECT id FROM people
            WHERE people.name = 'Jennifer Lawrence'
        )
)
AND id IN
(
SELECT s.movie_id
FROM stars AS s
WHERE person_id IN
    (
        SELECT id FROM people
        WHERE people.name = 'Bradley Cooper'
    )
);
