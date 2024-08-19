SELECT p.name, p.id, m.title as movies ,i.info, pi.info,aka.name as aka_name
FROM person p 
LEFT JOIN cast_info c ON p.id = c.person_id
LEFT JOIN person_info pi ON pi.person_id = p.id
LEFT JOIN info_type i ON i.id=pi.info_type_id
LEFT JOIN movie m ON c.movie_id = m.id
LEFT JOIN aka_name aka ON aka.person_id=p.id
WHERE (c.role_id = 1 or c.role_id = 2)
AND p.name ILIKE %s
ORDER BY p.name ASC;