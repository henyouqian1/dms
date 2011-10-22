DROP TABLE IF EXISTS Scores;
CREATE TABLE Scores (	user_id 	INTEGER NOT NULL,
						match_id 	INTEGER NOT NULL,
						score 		INTEGER NOT NULL,
						PRIMARY KEY (user_id, match_id)
						) ENGINE = InnoDB;
						
INSERT INTO Scores VALUES(1, 1, 200);
INSERT INTO Scores VALUES(1, 2, 1040);