SELECT movie.id, movie.title, movie.production_year, movie_rating.info
FROM movie
JOIN movie_rating ON movie.id = movie_rating.movie_id
JOIN info_type ON info_type.id = movie_rating.info_type_id
WHERE info_type.id = 101 
ORDER BY CAST(movie_rating.info AS DOUBLE PRECISION) DESC,movie.production_year DESC
limit 10;