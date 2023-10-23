SELECT count(DISTINCT C.CitingPaperID)
FROM Cites as C
JOIN Write as W ON C.CitedPaperID = W.PaperID
WHERE W.FNAME = 'Lei' AND W.LNAME = 'Yin';