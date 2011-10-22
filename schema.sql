DROP DATABASE IF EXISTS dms;
CREATE DATABASE dms DEFAULT CHARACTER SET utf8;
USE dms;

CREATE TABLE Users (	user_id 	INTEGER 	PRIMARY KEY AUTO_INCREMENT,
						name 		VARCHAR(20) NOT NULL,
						password 	VARCHAR(20) NOT NULL,
						email 		VARCHAR(30) NOT NULL,
						country 	SMALLINT 	NOT NULL
						)ENGINE = InnoDB;
						
CREATE TABLE Games (	game_id 		INTEGER 	PRIMARY KEY AUTO_INCREMENT,
						name 			VARCHAR(20) NOT NULL,
						big_is_better 	BOOLEAN 	NOT NULL,
						modify_datetime	DATETIME	NOT NULL
						)ENGINE = InnoDB;

CREATE TABLE Tournaments (	tournament_id 		INTEGER PRIMARY KEY AUTO_INCREMENT,
							match_num 			SMALLINT,
							begin_date			DATE,
							end_date			DATE,
							is_publish			BOOLEAN,	#是否已发布，如果是，用户可见,并且不可编辑，要修改需要先置为false然后重新公布
							version				SMALLINT	#用户判断是否看过或者有变动
							)ENGINE = InnoDB;
							
CREATE TABLE Matchs (	match_id 		INTEGER PRIMARY KEY AUTO_INCREMENT,
						tournament_id 	INTEGER,		#if null, simple dayly game
						game_id 		INTEGER NOT NULL,
						date 			DATE 	NOT NULL,
						prev_match_id 	INTEGER,
						pass_mode 		INTEGER NOT NULL,
						pass_value 		INTEGER NOT NULL,
						pass_score 		INTEGER
						)ENGINE = InnoDB;

CREATE TABLE Scores (	user_id 	INTEGER NOT NULL,
						match_id 	INTEGER NOT NULL,
						score 		INTEGER NOT NULL,
						time 		TIME 	NOT NULL,
						rank 		INTEGER,
						is_pass 	BOOLEAN
						)ENGINE = InnoDB;

