SELECT DISTINCT movie.id, movie.title, movie.production_year, 
COALESCE(movie_rating.info, 'unavailable') as rating, 
p1.name AS actor1_name, p2.name AS actor2_name
FROM movie
JOIN cast_info c1 ON movie.id = c1.movie_id
JOIN cast_info c2 ON movie.id = c2.movie_id
JOIN person p1 ON c1.person_id = p1.id
JOIN person p2 ON c2.person_id = p2.id
LEFT JOIN movie_info movie_rating ON movie.id = movie_rating.movie_id AND movie_rating.info_type_id = (SELECT id FROM info_type WHERE info = 'rating')
WHERE p1.id = %s 
AND p2.id = %s 
AND p1.id <> p2.id 
AND c1.role_id IN (1, 2)
AND c2.role_id IN (1, 2)
ORDER BY movie.id;
