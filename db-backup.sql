DROP TABLE IF EXISTS `Posts`;
CREATE TABLE `Posts` (
  `ptitle` varchar(140) NOT NULL,
  `comments` varchar(500) NOT NULL,
  `postid` int(11) NOT NULL AUTO_INCREMENT,
  `upvotes` int(11) NOT NULL,
  `ptext` varchar(8000) NOT NULL,
  `name` varchar(50) NOT NULL,
  `classs` varchar(50) NOT NULL,
  `sec` varchar(50) NOT NULL,
  `admno` varchar(50) NOT NULL,
  `upvotesid` varchar(8000) NOT NULL,
  PRIMARY KEY (`postid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
LOCK TABLES `Posts` WRITE;
/*EXAMPLE VALUES*/;
INSERT INTO `Posts` VALUES ('Title1','',8,3,'Post1','Praneet Shekhar','12','D','12345','startingvalue,secondstartingvalue,12345,17890,41207'),('Title2','',9,1,'Post2','Aakash Pahwa','12','D','41207','startingvalue,secondstartingvalue,41207'),('Title3','',10,2,'Post3','Name1','12','A','17890','startingvalue,secondstartingvalue,17890,41207'),('Title4','',11,0,'Post4','Aakash Pahwa','12','A','04321','startingvalue,secondstartingvalue');
UNLOCK TABLES;
DROP TABLE IF EXISTS `RegLog`;
CREATE TABLE `RegLog` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `classs` varchar(50) NOT NULL,
  `sec` varchar(50) NOT NULL,
  `admno` varchar(50) NOT NULL,
  `picc` int(11) DEFAULT '0',
  `postc` int(11) DEFAULT '0',
  `udc` varchar(6000) NOT NULL DEFAULT ',',
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
LOCK TABLES `RegLog` WRITE;
/*EXAMPLE VALUES*/;
INSERT INTO `RegLog` VALUES (1,'Aakash Pahwa','12','D','41207',1,1,',10,9,8'),(2,'Praneet Shekhar','12','D','12345',1,1,',8'),(3,'Anubhav Kumar Singh','12','D','00000',0,0,''),(4,'Name1','12','A','17890',1,1,',10,8'),(5,'Aakash Pahwa','12','A','04321',1,1,',');
UNLOCK TABLES;