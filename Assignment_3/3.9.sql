SELECT FNAME, LNAME
FROM Write
GROUP BY FNAME, LNAME
HAVING COUNT(*) = 1;