SELECT movie.id, movie.title AS movie_title, company.name, movie.production_year, movie_type.kind
FROM movie
LEFT JOIN movie_company ON movie.id = movie_company.movie_id
JOIN company ON company.id = movie_company.company_id
LEFT JOIN movie_type on movie.kind_id = movie_type.id
WHERE company.name ILIKE %s
AND movie_company.company_type_id = 2;