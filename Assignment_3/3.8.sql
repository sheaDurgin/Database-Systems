SELECT P.Title
FROM Paper as P
WHERE P.ID IN (SELECT W.PaperID
               FROM Write as W
               GROUP BY W.PaperID
               HAVING COUNT(W.PaperID) = 1);