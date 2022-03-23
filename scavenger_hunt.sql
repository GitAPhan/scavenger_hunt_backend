-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: scavenger_hunt
-- ------------------------------------------------------
-- Server version	5.5.5-10.7.3-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `check_in`
--

DROP TABLE IF EXISTS `check_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `check_in` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `game_id` int(10) unsigned NOT NULL,
  `checkpoint_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `is_winner` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `check_in_FK` (`checkpoint_id`),
  KEY `check_in_FK_1` (`game_id`),
  KEY `check_in_FK_2` (`user_id`),
  CONSTRAINT `check_in_FK` FOREIGN KEY (`checkpoint_id`) REFERENCES `checkpoint` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `check_in_FK_1` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `check_in_FK_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `check_in`
--

LOCK TABLES `check_in` WRITE;
/*!40000 ALTER TABLE `check_in` DISABLE KEYS */;
INSERT INTO `check_in` VALUES (26,3,1,16,-1,'2022-03-18 23:13:52'),(33,3,1,16,1,'2022-03-19 01:57:53'),(36,3,1,16,1,'2022-03-19 02:50:17'),(37,3,2,16,0,'2022-03-19 02:50:36'),(38,3,2,16,-1,'2022-03-19 02:50:40'),(39,3,2,16,1,'2022-03-19 02:53:40'),(40,3,2,16,1,'2022-03-19 09:52:05'),(41,3,2,16,1,'2022-03-19 09:52:17'),(42,3,4,16,1,'2022-03-19 16:48:57'),(43,3,4,16,0,'2022-03-19 16:49:03'),(44,3,4,16,-1,'2022-03-19 16:49:07'),(45,3,4,16,1,'2022-03-19 16:49:12'),(46,3,4,16,1,'2022-03-19 16:49:16'),(47,3,4,16,1,'2022-03-19 16:49:21'),(48,3,5,16,1,'2022-03-19 16:57:27'),(51,3,5,1,0,'2022-03-20 22:54:33'),(52,3,5,1,1,'2022-03-20 22:54:53'),(53,3,7,1,-1,'2022-03-20 23:14:34'),(54,3,1,1,1,'2022-03-20 23:20:25'),(55,3,1,1,0,'2022-03-20 23:20:34'),(56,3,1,1,-1,'2022-03-20 23:20:38'),(57,3,1,21,0,'2022-03-20 23:22:47'),(58,3,1,21,0,'2022-03-20 23:22:50'),(59,3,1,21,1,'2022-03-20 23:22:54'),(60,3,5,21,1,'2022-03-20 23:25:38'),(61,3,5,21,0,'2022-03-20 23:25:38'),(62,3,5,21,0,'2022-03-20 23:25:38'),(63,3,5,16,1,'2022-03-20 23:25:38'),(64,3,5,16,1,'2022-03-20 23:25:38'),(65,3,5,1,0,'2022-03-20 23:25:38'),(66,3,4,21,1,'2022-03-20 23:25:38'),(67,3,4,21,1,'2022-03-20 23:25:38'),(68,3,1,29,0,'2022-03-21 12:32:59'),(69,3,1,29,0,'2022-03-21 12:33:08'),(71,3,1,29,0,'2022-03-21 12:36:51'),(72,3,6,21,0,'2022-03-21 17:26:10'),(73,3,2,29,-1,'2022-03-21 18:02:58'),(74,3,2,29,-1,'2022-03-21 18:03:01'),(75,3,2,29,-1,'2022-03-21 18:03:05'),(76,3,2,29,0,'2022-03-21 18:03:07'),(77,3,2,29,0,'2022-03-21 18:03:12'),(78,3,4,29,1,'2022-03-21 18:16:49'),(79,3,4,29,-1,'2022-03-21 18:16:54'),(80,3,4,29,0,'2022-03-21 18:17:02'),(81,3,4,29,0,'2022-03-21 18:17:06'),(82,3,4,29,1,'2022-03-21 18:17:13'),(83,3,4,29,0,'2022-03-21 18:17:16'),(84,3,4,1,1,'2022-03-22 11:22:56'),(85,3,4,1,1,'2022-03-22 11:22:59'),(86,3,4,1,0,'2022-03-22 11:23:04'),(87,3,4,1,0,'2022-03-22 11:23:08'),(88,3,4,1,-1,'2022-03-22 11:23:12'),(89,3,4,1,-1,'2022-03-22 11:23:17'),(90,3,2,1,-1,'2022-03-22 11:24:22'),(91,3,2,1,1,'2022-03-22 11:24:25'),(92,3,2,1,0,'2022-03-22 11:24:31'),(93,3,2,1,0,'2022-03-22 11:24:34'),(94,3,2,1,0,'2022-03-22 11:24:39'),(95,3,6,1,0,'2022-03-22 12:23:59'),(96,3,6,1,0,'2022-03-22 12:24:10'),(97,3,6,1,1,'2022-03-22 12:25:29'),(98,3,6,1,-1,'2022-03-22 12:25:51'),(99,3,5,29,-1,'2022-03-22 14:01:15'),(100,3,5,29,0,'2022-03-22 14:01:19'),(101,3,5,29,0,'2022-03-22 14:01:23'),(109,3,8,29,-1,'2022-03-22 14:21:33'),(110,3,8,29,0,'2022-03-22 14:21:40'),(113,3,8,29,1,'2022-03-22 14:27:04'),(114,3,4,21,-1,'2022-03-22 16:52:32'),(115,3,4,21,1,'2022-03-22 16:52:38'),(116,3,4,21,0,'2022-03-22 16:52:43'),(117,3,4,21,1,'2022-03-22 16:52:49');
/*!40000 ALTER TABLE `check_in` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `checkpoint`
--

DROP TABLE IF EXISTS `checkpoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `checkpoint` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `game_id` int(10) unsigned NOT NULL,
  `token_reward` tinyint(3) unsigned NOT NULL,
  `point_reward` smallint(5) unsigned NOT NULL,
  `rounds` tinyint(3) unsigned NOT NULL,
  `game_type` tinyint(3) unsigned NOT NULL,
  `name` varchar(100) NOT NULL,
  `check_token` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `checkpoint_un` (`check_token`),
  KEY `checkpoint_FK` (`game_id`),
  CONSTRAINT `checkpoint_FK` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checkpoint`
--

LOCK TABLES `checkpoint` WRITE;
/*!40000 ALTER TABLE `checkpoint` DISABLE KEYS */;
INSERT INTO `checkpoint` VALUES (1,3,1,300,3,0,'Mt. Fuji','kldaht803yawjnlahg[ay[y3tva'),(2,3,2,400,5,0,'Mt. Everest','test'),(4,3,1,450,6,0,'Mt. Helena','tester'),(5,3,2,350,3,0,'Mt. George','testing'),(6,3,3,375,4,0,'Mt. Wyatt','new'),(7,3,4,1000,1,0,'Mt. Short','short'),(8,3,2,750,3,0,'Mt. Tall','tall');
/*!40000 ALTER TABLE `checkpoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `game_token` varchar(10) NOT NULL COMMENT 'game master',
  `user_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `start_time` datetime DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `game_un` (`game_token`),
  KEY `game_FK` (`user_id`),
  CONSTRAINT `game_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `game` VALUES (1,'673f37',27,'2022-03-16 18:17:08',NULL,NULL,'helloGame'),(2,'e1847e',1,'2022-03-16 18:20:06',NULL,NULL,'helloGame'),(3,'0300dd',16,'2022-03-16 18:47:11',NULL,NULL,'helloGame'),(4,'232108',1,'2022-03-17 00:06:43',NULL,NULL,'newGame'),(5,'164961',1,'2022-03-17 00:31:58',NULL,NULL,'newGamef'),(6,'347cb0',1,'2022-03-17 12:03:30',NULL,NULL,'lets begin');
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `value` tinyint(3) unsigned NOT NULL,
  `description` varchar(225) NOT NULL,
  `checkpoint_id` int(10) unsigned NOT NULL,
  `type` varchar(100) NOT NULL,
  `game_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `item_FK` (`game_id`),
  KEY `item_FK_1` (`checkpoint_id`),
  CONSTRAINT `item_FK` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `item_FK_1` FOREIGN KEY (`checkpoint_id`) REFERENCES `checkpoint` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `game_id` int(10) unsigned DEFAULT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `login_token` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `player_token` varchar(100) DEFAULT NULL,
  `master_token` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_un` (`login_token`),
  UNIQUE KEY `user_game_un` (`user_id`,`game_id`),
  UNIQUE KEY `player_un` (`player_token`),
  UNIQUE KEY `gm_un` (`master_token`),
  KEY `login_FK` (`game_id`),
  CONSTRAINT `login_FK` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `login_FK_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (37,3,16,NULL,'2022-03-19 17:50:06','M8ytgEPG5vJMzYqQykrELlYQ98qOKhAi3ZnmCm8AQY2-hsh7dwvndrnk_JYoVvbZ_M-4Fy9KobQLYkH8F2hjHg',NULL),(74,3,29,NULL,'2022-03-22 14:04:43','niYHysOKezliM1hCEkW4vUUXtErRLsjYNR1DmnYGHIHX6BlBxIBD2O4_YKixEcVTDWoCP2q6rUz_9nG5wmhD7Q',NULL),(76,3,1,NULL,'2022-03-22 16:57:44','TQfs561r_2FjzHwVoQlmamj6FrFFjrpOHDuyUbgE71e8rhhl0SpNh3IIh6pqmb1a9QkPfO1Y3w8SwiiXSYL_vA',NULL),(77,NULL,1,'4Gqv83HQ50iEfipBxYsX7WwWUm_qhWr7meICxE4JQ6sBq83HzYMflB4E8inP7nGPWR0','2022-03-22 21:02:35',NULL,NULL);
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `token` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `token` varchar(100) NOT NULL,
  `game_id` int(10) unsigned NOT NULL,
  `check_in_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_un` (`token`),
  KEY `token_FK` (`check_in_id`),
  KEY `token_FK_1` (`game_id`),
  KEY `token_FK_2` (`user_id`),
  CONSTRAINT `token_FK` FOREIGN KEY (`check_in_id`) REFERENCES `check_in` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `token_FK_1` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `token_FK_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `item_id` int(10) unsigned NOT NULL,
  `token_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `game_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `transaction_un` (`item_id`,`user_id`,`game_id`),
  KEY `transaction_FK` (`game_id`),
  KEY `transaction_FK_1` (`user_id`),
  KEY `transaction_FK_3` (`token_id`),
  CONSTRAINT `transaction_FK` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `transaction_FK_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `transaction_FK_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `transaction_FK_3` FOREIGN KEY (`token_id`) REFERENCES `token` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `password` varchar(150) NOT NULL,
  `salt` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `email` varchar(150) NOT NULL,
  `is_over_13` tinyint(1) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_un` (`username`),
  UNIQUE KEY `user_uni` (`email`),
  CONSTRAINT `user_check` CHECK (octet_length(`username`) >= 8)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'username','ade69a043dec5ec005a5aa3817f4ef6cb1ff284af256e313b82974176c72805e03f5f8e6fbd73c24ea6d5885687d48e800c66d02ee75ea0d8a5fcffad269d34f','O1mAMNBUGU79MQ','2022-03-15 12:11:53','email',1,NULL),(16,'userTest','dddcb1ea4830d92744af92a919bb25b2f3dfd4277ebef350cda3299c5f513a6d4f41e922635f4340bfa2ac0be77ae0216b95072b99e8dc9f994f6e03d78ffd4e','xdlfAKXAgmUAuw','2022-03-15 15:58:20','email@',1,NULL),(21,'userTest2','a42c0dadc5ca23b942cd48e09dac7776bf1fe8af01e04fec8faf014613a710a0801772a2364edabca578a245260000c7862066a63a735389fe19e5099f689fe0','wEtrbXpQMMKsgA','2022-03-15 16:05:53','email@2',1,'name'),(22,'userTest22','9f608c2b7da490c181563e119599276cbdf42ef2d04f19596b4369481ec991cfa4158ca2680d8738fc95b3a15195f498a40aca02055f4b7ffa44dc8e8ecf3718','vMFszGTswygrYw','2022-03-15 16:55:49','e@mail.ca',1,NULL),(23,'userTest33','231823df71d20bf9be3346f7b98bc289777d088094cbed845e5e967afb32efe297ded541ad5a292a9574f581195aea3b232d8d6b86ace058ed20296816041801','72a_UgESAlusCg','2022-03-15 16:59:01','e@mai.com',1,'NAMES'),(24,'newTEster','ccaab07fdd7b7025bfa5320c43f62bc1815599c5385a072a239329e29c9dd3c02a302c01fe6f52d1ac7277ffdd05826c6753510048d1fc04326dd8bba7d8cbba','q5N7QWuzut7wEg','2022-03-15 17:00:50','email@mail.com',1,'new name'),(25,'testPlayer','717a939cd3c3d2f8cd2baa1da9ac8fdaeed85c15d6e3169864e11114db4db18e9cb0fa5994b9fdcddc8e875f53c7184a8ef62bdc6c7d80768119ce4ada42f90e','vzlvd3eb_gPIvQ','2022-03-15 19:18:42','e@admin.com',1,'AdminPlayer'),(26,'Player01','a1f2ab46fbab5395ee7779ed6c5d70153bc746bd631c1cefd7509a2fc7f7cbca0f67502cb0fd9956dbd97037ab60a1dbb06c8507146ac8bd6f48864f09d3095c','BVixJdrNTu7PdA','2022-03-15 19:22:23','d@email.com',1,'test player'),(27,'loginTest','e1b8f28947751a0c4cf43c64f1884a09a260337ea0f4a4808c9af2bd39bb57c8561ffcc58d6bd208c56dd53b30fb940744109e12958b2cb6453d3b19907cdf2d','qiFpMItscz2YYQ','2022-03-16 13:49:43','emai@l.com',1,'dummy'),(28,'thePlayer','1376a8a0de4144a4f754d28c47d70c047092ae5c6f42f3ec444b9828bebb9f1d34aad0f0117cf2d22eb0fea88d491c46164d92fea20feaf8a6c52d069fb2646c','EDMC2yA0HtRmBg','2022-03-16 22:40:52','enm@hgao.com',1,'joingame'),(29,'playerTest','944d039aefaaa31a6aa5f30f7609630d1eab78b1521f7a9ed6659e410070681b31ac71641dfbdfea178bd8f9b8ae92c5ee30b6521f7df50686528ffa42f95075','0FgLPC5Gw3H8iQ','2022-03-21 11:43:55','emai@mail.com',1,'ADMIN');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'scavenger_hunt'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-22 21:05:25
