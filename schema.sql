DROP DATABASE IF EXISTS dms;
CREATE DATABASE dms DEFAULT CHARACTER SET utf8;
USE dms;

CREATE TABLE Users (	user_id 	INTEGER(20)	PRIMARY KEY AUTO_INCREMENT,
						email 		VARCHAR(40) NOT NULL,
						password 	CHAR(64) 	NOT NULL,
						name 		VARCHAR(20) NOT NULL,
						country 	SMALLINT 	NOT NULL,
						facebook_id	INTEGER(20),
						UNIQUE KEY email_unique (email),
						UNIQUE KEY facebook_id_unique (facebook_id)
						)ENGINE = InnoDB;
						
CREATE TABLE Games (	game_id 			INTEGER(20) 	PRIMARY KEY AUTO_INCREMENT,
						name 				VARCHAR(20) NOT NULL,
						score_small_better 	BOOLEAN 	NOT NULL,
						modify_datetime		DATETIME	NOT NULL
						)ENGINE = InnoDB;

CREATE TABLE Tournaments (	tournament_id 		INTEGER(20) PRIMARY KEY AUTO_INCREMENT,
							title				VARCHAR(40),
							description			VARCHAR(200),
							match_num 			SMALLINT NOT NULL,
							begin_date			DATE,
							end_date			DATE,
							is_publish			BOOLEAN,	#是否已发布，如果是，用户可见,并且不可编辑，要修改需要先置为false然后重新公布
							modify_datetime		DATETIME	#用户判断是否看过或者有变动
							)ENGINE = InnoDB;
							
CREATE TABLE Matchs (	match_id 		INTEGER(20) PRIMARY KEY AUTO_INCREMENT,
						tournament_id 	INTEGER(20),		#if null, simple dayly game
						game_id 		INTEGER(20) NOT NULL,
						date 			DATE 	NOT NULL,
						prev_match_id 	INTEGER,
						pass_mode 		INTEGER NOT NULL,
						pass_value 		INTEGER NOT NULL,
						pass_score 		INTEGER
						)ENGINE = InnoDB;
						
CREATE TABLE Dailymatchs (	dailymatch_id 	INTEGER(20) PRIMARY KEY AUTO_INCREMENT,
							game_id 		INTEGER(20) NOT NULL,
							developer_id 	INTEGER(20) NOT NULL,
							date 			DATE 		NOT NULL,
							title			VARCHAR(100),
							description		VARCHAR(200),
							status			ENUM('edit','open','close') NOT NULL
						)ENGINE = InnoDB;
	
CREATE TABLE Awards (	award_id 		INTEGER(20) PRIMARY KEY AUTO_INCREMENT,
						developer_id 	INTEGER(20) NOT NULL,
						name			VARCHAR(40) NOT NULL,
						description		VARCHAR(200),
						image			VARCHAR(100)
						)ENGINE = InnoDB;

CREATE TABLE Scores (	user_id 		INTEGER NOT NULL,
						dailymatch_id 	INTEGER NOT NULL,
						score 			INTEGER NOT NULL,
						time 			TIME 	NOT NULL,
						rank 			INTEGER,
						)ENGINE = InnoDB;

CREATE TABLE Developers (	developer_id 	INTEGER(20)	PRIMARY KEY AUTO_INCREMENT,
							email 		VARCHAR(40) NOT NULL,
							password 	CHAR(64) 	NOT NULL,
							UNIQUE KEY email_unique (email)
							)ENGINE = InnoDB;