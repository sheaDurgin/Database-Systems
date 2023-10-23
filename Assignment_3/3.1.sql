SELECT P.Title
FROM Paper AS P
JOIN Write AS W ON P.ID = W.PaperID
WHERE W.FNAME = 'Minoru' AND W.LNAME = 'Eto'
ORDER BY P.LastUpdate DESC;
