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
  `rounds_won` tinyint(3) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `check_in_un` (`game_id`,`checkpoint_id`,`user_id`),
  KEY `check_in_FK_1` (`checkpoint_id`),
  KEY `check_in_FK_2` (`user_id`),
  CONSTRAINT `check_in_FK` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `check_in_FK_1` FOREIGN KEY (`checkpoint_id`) REFERENCES `checkpoint` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `check_in_FK_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `game_type` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `checkpoint_FK` (`game_id`),
  CONSTRAINT `checkpoint_FK` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `game_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `login_token` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_un` (`login_token`),
  KEY `login_FK` (`game_id`),
  KEY `login_FK_1` (`user_id`),
  CONSTRAINT `login_FK` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `login_FK_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(150) NOT NULL,
  `salt` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `email` varchar(150) NOT NULL,
  `birthdate` date NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_un` (`username`),
  UNIQUE KEY `user_uni` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

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

-- Dump completed on 2022-03-11 17:28:27
