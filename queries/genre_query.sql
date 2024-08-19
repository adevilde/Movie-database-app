SELECT m.id, m.title, movie_type.kind, 
m.production_year,
movie_rating.info AS rating
FROM movie m
LEFT JOIN movie_type ON movie_type.id=m.kind_id
JOIN info_type i1 ON i1.info = 'genres'
JOIN info_type i2 ON i2.info = 'rating'
LEFT JOIN movie_info ON m.id = movie_info.movie_id AND i1.id = movie_info.info_type_id
LEFT JOIN movie_rating ON m.id = movie_rating.movie_id AND i2.id = movie_rating.info_type_id
WHERE movie_info.info ILIKE %s
AND movie_rating.info IS NOT NULL
ORDER BY CAST(movie_rating.info AS DOUBLE PRECISION) DESC
LIMIT 10;