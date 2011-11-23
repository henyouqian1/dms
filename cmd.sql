CREATE TABLE Awards (	award_id 		INTEGER(20) PRIMARY KEY AUTO_INCREMENT,
						developer_id 	INTEGER(20) NOT NULL,
						name			VARCHAR(40) NOT NULL,
						description		VARCHAR(200),
						image			VARCHAR(100)
						)ENGINE = InnoDB;