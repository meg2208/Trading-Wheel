Select Distinct 
	Q.security, 
	SUM(Q.volume)
FROM 
	query_data Q
WHERE
	extract(year from Q.time) = 2009
GROUP BY 
	Q.security;
