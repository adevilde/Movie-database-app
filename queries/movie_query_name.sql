SELECT distinct movie.title, movie.id, i1.info as info_type, movie_info.info, movie_type.kind,
       movie.production_year, person.name as cast_names, 
       i2.info as rating_info_type,
       COALESCE(movie_rating.info, 'unavailable') as rating_info,
       COALESCE(company.name, 'unavailable') as company_name
FROM movie
JOIN movie_info ON movie.id = movie_info.movie_id
JOIN info_type AS i1 ON i1.id = movie_info.info_type_id
JOIN movie_type ON movie.kind_id = movie_type.id
JOIN cast_info ON cast_info.movie_id = movie.id
JOIN person ON cast_info.person_id = person.id
LEFT JOIN movie_rating ON movie.id = movie_rating.movie_id
LEFT JOIN info_type as i2 ON i2.id = movie_rating.info_type_id
LEFT JOIN movie_company ON movie.id = movie_company.movie_id
LEFT JOIN company ON movie_company.company_id = company.id
WHERE movie.title ILIKE %s
AND i1.id = movie_info.info_type_id
order by movie.id;
