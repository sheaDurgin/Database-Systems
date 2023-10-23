SELECT COUNT(*)
FROM Write
WHERE (FNAME = 'Indranath' AND LNAME = 'Sengupta')
AND PaperID IN (
    SELECT PaperID
    FROM Write
    GROUP BY PaperID
    HAVING COUNT(PaperID) < 3
  );