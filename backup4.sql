-- MySQL dump 10.13  Distrib 9.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `access`
--

DROP TABLE IF EXISTS `access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `access` (
  `id` int NOT NULL,
  `access_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Ð”Ð»Ñ ÑƒÐºÐ°Ð·Ð°Ð½Ð¸Ñ ÑƒÑ€Ð¾Ð²Ð½Ñ Ð´Ð¾ÑÑ‚ÑƒÐ¿Ð°';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access`
--

LOCK TABLES `access` WRITE;
/*!40000 ALTER TABLE `access` DISABLE KEYS */;
INSERT INTO `access` VALUES (1,'Ð‘Ð°Ð·Ð¾Ð²Ñ‹Ð¹'),(2,'ÐŸÐ¾Ð²Ñ‹ÑˆÐµÐ½Ð½Ñ‹Ð¹'),(3,'ÐÐ´Ð¼Ð¸Ð½');
/*!40000 ALTER TABLE `access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content`
--

DROP TABLE IF EXISTS `content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `content` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `file_path` varchar(255) NOT NULL,
  `access_level` int NOT NULL,
  `department_id` int NOT NULL,
  `tag_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_content_access` (`access_level`),
  KEY `fk_content_department` (`department_id`),
  KEY `fk_content_tag` (`tag_id`),
  CONSTRAINT `fk_content_access` FOREIGN KEY (`access_level`) REFERENCES `access` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_content_department` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_content_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Ð¢Ð°Ð±Ð»Ð¸Ñ†Ð° Ð´Ð»Ñ Ñ…Ñ€Ð°Ð½ÐµÐ½Ð¸Ñ ÐºÐ¾Ð½Ñ‚ÐµÐ½Ñ‚Ð°';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content`
--

LOCK TABLES `content` WRITE;
/*!40000 ALTER TABLE `content` DISABLE KEYS */;
INSERT INTO `content` VALUES (32,'1234','1','Research\\3/1_1_Ð˜Ð½ÑÑ‚Ñ€ÑƒÐºÑ†Ð¸Ñ_Ð¿Ð¾_ÐºÐ¾Ð¼Ð¿Ð»ÐµÐºÑ‚Ð°Ñ†Ð¸Ð¸_Ð³Ð¾Ñ‚Ð¾Ð²Ð¾Ð¹_Ð¿Ñ€Ð¾Ð´ÑƒÐºÑ†Ð¸Ð¸.docx',3,5,1),(33,'2','2','Research\\3/1. Ð ÐµÑˆÐµÐ½Ð¸Ðµ Ð¾Ð¿ÐµÑ€Ð°Ñ‚Ð¸Ð²Ð½Ñ‹Ñ… Ð·Ð°Ð´Ð°Ñ‡.html',3,5,1),(34,'123','123','Research\\3/Ð˜Ð½ÑÑ‚Ñ€ÑƒÐºÑ†Ð¸Ñ Ð¿Ð¾ ÐºÐ¾Ð¼Ð¿Ð»ÐµÐºÑ‚Ð°Ñ†Ð¸Ð¸ Ð¿Ñ€Ð¸Ð±Ð¾Ñ€Ð¾Ð² Ð½Ð° ÑÐºÐ»Ð°Ð´ Ð³Ð¾Ñ‚Ð¾Ð²Ð¾Ð¹ Ð¿Ñ€Ð¾Ð´ÑƒÐºÑ†Ð¸Ð¸ Ðº Ð‘ÐŸ-18.pdf',3,5,1);
/*!40000 ALTER TABLE `content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `id` int NOT NULL,
  `department_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Ð”Ð»Ñ ÑƒÐºÐ°Ð·Ð°Ð½Ð¸Ñ Ð¾Ñ‚Ð´ÐµÐ»Ð°';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'ÐšÐ»Ð¸ÐµÐ½Ñ‚Ñ‹'),(2,'Ð¡ÐµÑ€Ð²Ð¸ÑÐ½Ð°Ñ ÑÐ»ÑƒÐ¶Ð±Ð°'),(3,'ÐžÑ‚Ð´ÐµÐ» Ð¿Ñ€Ð¾Ð´Ð°Ð¶'),(4,'ÐžÑ‚Ð´ÐµÐ» Ð¼ÐµÑ‚Ð¾Ð´Ð¸Ðº'),(5,'ÐÐ´Ð¼Ð¸Ð½');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `text` varchar(255) NOT NULL,
  `photo` blob,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_feedback_id` (`id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,10,'Ð¿Ñ€Ð¸Ð²Ð•Ð¢',_binary 'PK\0\0\0\0\0!\0ß¤\ÒlZ\0\0 \0\0\0[Content_Types].xml ¢( \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0´”\Ën\Â0E\÷•ú‘·Ubè¢ª*‹>–-R\é{Vý’Ç¼þ¾QU‘\nl\"%3\÷\Þ3VÆƒ\ÑÚšl	µw%\ë=–“^i7+\Ù\×\ä-d&\á”0\ÞA\É6€l4¼½L60#µÃ’\ÍS\nOœ£œƒXø\0Ž*•V$z3„ü3\à\÷½\Þ—\Þ%p)Oµ^ “²\×5}nH\"d\Ùs\ÓXg•L„`´‰\ê|\éÔŸ”|—PrÛƒs\ðŽ\Z?˜PWŽ\ìtt4Q+\È\Æ\"¦wa©‹¯|T\\y¹°¤,N\Û\à\ôU¥%´ú\Ú-D/‘\ÎÜš¢­X¡Ýžÿ(¦¼<E\ã\Û)‘\à\Z\0;\çN„L?¯F\ñË¼¤¢Ü‰˜\Z¸<Fk\Ý	‘h¡y\ö\Ï\æ\ØÚœŠ¤\Îq\ôi£\ã?\ÆÞ¯l­\Îi\à\01\é\Ó]›H\Ög\Ï\õm @\È\æ\Ûûmø\0\0ÿÿ\0PK\0\0\0\0\0!\0‘\Z·\ï\0\0\0N\0\0\0_rels/.rels ¢( \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0¬’Áj\Ã0@\ïƒýƒÑ½Q\ÚÁ£N/c\Ð\Û\Ù[IL\Û\Øj\×þý<\Ø\Ø]\éaG\Ë\ÒÓ“\ÐzsœFu\à”]\ð\Z–U\rŠ½	\Öù^\Ã[û¼x\0•…¼¥1x\Öp\â›\æ\öfý\Ê#I)Êƒ‹YŠ\Ï\Z‘øˆ˜\ÍÀ\å*D\ö\å§i\")\Ï\Ôc$³£žqU\×\÷˜~3 ™1\Õ\ÖjH[{ª=E¾†º\Î~\nf?±—3-\ÂÞ²]\ÄTê“¸2j)\õ,\Zl0/%œ‘b¬\n\Z\ð¼\Ñ\êz£¿§Å‰…,	¡	‰/û|f\\Zþ\çŠ\æ?6\ï!Y´_\áoœ]A\ó\0\0ÿÿ\0PK\0\0\0\0\0!\0qû°\ò\0\0\óU\0\0\0\0word/document.xml\ì][oG–~_`ÿ¡§`$vWß…±}	;™y\\PdK\âšdÍ–eÏ“\å$\ëØ›™É¬7\ãø’\Í\Ã²-%²,\É@~A\ñ/\Ì/\Ù:\Õ\Ý\Ù\"¥%J¼v7‹¬\Ó]§\ÎW\çRU§~ý›;\õZ\á¶¶ªA\ãÚœ¸ \ÌüF9¨T«\×\æ>ùØ›\×\ç\n­¨Ô¨”jAÃ¿6w\×o\Íýf\é_ÿ\å\×‹• ¼^\÷Q‘h´7š\åkskQ\Ô\\,[\å5¿^j-Ô«\å0h+\ÑB9¨ƒ••j\Ù/na¥HQ\àw\Í0(û­{ž]j\Ü.µ\ær\å;ù¨U\Â\Ò«\åby­Fþ#\Zâ™‰(E£¨\'D† \ÄZH\Äã¤¤3“R‹\ðV\Ç\ÉCbouŒ’2¥>S‡£DŽSÒ†£$§¤G\é˜8Õx\Ð\ô\ìË• ¬—\"\ö1\\-\ÖK\á­\õ\æ<#\Ü,E\Õ\åj­\Z\Ýe45%Sª6n\r\ñF¬V‡B]ªœ™‚V¬¿&UR*Áµ¹\õ°±˜ÔŸ\ïÔ‡W_Œ\ë\'—N\r¿–\ï±\ìqFÑ¿\ÕZQZ7\ÌÃ»¸º“,œk\ÅÐ¯1>\ÖZµ\Ù\ê\ÃRc_®¥DnŸÄ€\Û\õZú»¦˜jƒ†6\'\î†#‚y^?\é»z-~\ó“)ŠBŽ\Þ\Zy^¡\÷™\é›Ô™=x(\Öt1W\Ì9ø¤\È1j\ÙÏ©,R\ZzB£X>B7Ð©\æ„UJ\'\î S=b¬˜sÌ¾L\Êú™H)}¸@\õ.Z­JTY;¹´ŠP·•\ÖJ­hbŠ+9‚”¢\ÜE1°ZP\îŒg@\Ó?Ó”Á»\õ®>l®ž¨¿\rƒ\õ\æµ\êù¨}p4do€\ñtZ	\à»¡\Öù^\æ\æZ©\ÉF\òzy\ñƒ\ÕF––k\ì|\Þ\ð?d¸\ð[ÿ/ùInVjpSY/À8·ÄŒÀ\å r®M\ö…¼\Ø,…¥†TÝ´Á1\æx)S¡”j\ÉVº\È\ÎÊks‚@,B¡St=„B\Ý$¦ v\n¥´^‹ŽÿüzW‹\ë!\\6ª•`\Ã\ZQ°^¼]b\Ò*\Ì\á«V³Tf\Ì`¥¥•È‡‡­Zº‡È7Ö;¥\õ(ˆ«ý{9¥Sfª\Ä\ã\Ò0~\\\è±Gµ€d«\\e\"\óqµ\î·\n¿\÷7\n7‚z©4ýR+2[\ÕR\ß/\×\ÌF«O5þˆ\åø­¥\æ\ÇÁoC\èœ\Þ\æü)- zZbÃ«\ô”\ÕJ¼\ÅG/®\Ï\ßø¾+&(vx\ö\í‰\éj\í\Æ\"wZ¸0°nn†~\ËoûsK\ô%Ý¢t¯}ž>§;\íû\ì\ß=úªý)ûÿM{“\î\ÑCºS o\èa{³ý)Ý¦[\í{\ì\î>}MwX½ƒø\ëW\í/\ØW?\òúI\Ñ{F\à°ý+\ÚddvY\á{Ò»\ö£\ô‡¬\Ö=V\ô»{\ÍÈ²\'w}\Í^\àûz‡\Ý\æO\Úe…Ðœ(nTÜ\ÇqH\ÓÐ´+\Ã\á-\ßoþž=”w\ËÔr\Ùn\Í 8/­\ÕAZøùú˜Aq‹caŸî¶¿d\0\á\Ûb\Øy„rœ2\Ü\Ñ\íºo~\0£mø\ð+\ö^g›\Ãù>ÿ\énŠ¼\Ö[º\Ë\àË€û€£r\÷\çw9p§*ªfKB\ÜM\î\Ò>Ž–k\É%‘\Ï\å\Ú\Í\èn\ÍO)‹1aVüGV´‘°3º\Û\ì\áû\Úb†™¶ø§ ™Vo\r*´þ”\ÔL$Ÿß—ƒZv“©ù+\Ñp5—ƒ(\n\ê\Ã\Õ\r««kC>¶\Êúµ\âÿ\î<•ÿ0Le@k/Ë—kÁ­Ž\Ð\È&¯¶R\r[Ñ`ú±\0\â‘|:ú\Òj\ëuˆ’¦ß§ü\'\àwV©Q\é|úCü‰Eü©™…\ÛUvµ9*\ÙsdY0\â\Æ\ö‹‚šˆuO±¤\ë\ê\å”`r-]Ã•\à8¦%ˆN\\:h¸ú8®O$\Û!|´‰\Ê\ñÿI»Ê‰\ÔËŠ\0_\"ø•;¥\ô=“\ö•Š¨IŽA¼“Ÿ}ACe\×ËŸq¨\Ö#\n?¼ý\â†½Y10.Ã¤\0ÿý+ý3!\à\î+vý–>Ë£\ÓeÅ³QEAEA½A=\0\ã\ó\'funr‹\Ó]fŒ¶ÿƒ]\ö˜™Ž\"Ø´Ü´38v-wsÈ²¬É¶fˆ&\Ê2\Ê\ò¥\È2„7þ’T>\ç\î\Ùˆ…0\Ñ\Ým^`\Ò\r\Ò‚ýž	\ö.=(\äcÅ²]Ë´O±[PŒQŒ/HŒ\ã‘\ö}ûQû‹$6x\Ð~\È¸#×‡|\\~\ÃDømù%²+J¦—X\ã(¿(¿#–\ß\çq\ô+µ(\ÒXW\ë\×3\\\Ï2q¨EQ½º\È\ï¿uý\éþ\èb	0DsUOœ†\Ð\'\ô\åB–\Í0V\Ü8\Ç`ZM¿V»•\Â(\Ãt\ój‰þ/\ÌØ±Ÿƒ-I·r\ñ\ÇmT:ý&‘!\Ì4-þpø»:´ƒú>dJû¢\ï\nÿü\ì\ïyf\Ù\ÕWCo…\÷R†ßŸ\0ý\ó».mM„“Ôµ.Š\ÄP§Šd\Ú\Ú\Ë\Ëü\Æü\'7{_¦o\ë\åA­Ÿ^\×\ê\ÍBŽ‘XQtATtøO˜ã¿š\Ù}\è»d:3þ?\é\ØtRS%^=ß¤&q,—Y‹PûùŠ5n¾þ•Œ³\ô¯ ššA\Ü\ËYW‡ý‹\î@_w\à\èw\ô+ú5}AÿNÿF\Óÿ\Ë\ã¨Še™\îik=PtQt/\È0ú/ºE\÷\â9>ˆ>\ï\ë.aY\åaI\ñSú\"\àÚ¢¤\É®¿@Á\Ïtþ°\ë\ô‚ý\Ùýj~Ÿ,HyÀ\àþúbÂ¯ª­kšŽ\Ø{:\ÛCše(¶­\'±‡pt\ã45øÄ€\â\Î\áa±ÿ@\ËF>IRU4ƒ\Ç5„—¸,\Ù/\Ô\Û¢a\Ïs.§ÿ’¢!ú·†\Ã\ÉQMr9«Ž\÷\ñ,n—øn¨\Þ\îL\Ë&\Ærº¤\Ö&a™\Ç<hø-}B¿.°\Ë\ãûü„>§ÿ \Ï\èSV\ðý\ïûø‚}üš~C¿Ë¡œ]t-\ÓŸÁŸ~Ç8®¥™B\ÖqSS=2®]&©\Üe\ëi¤e©ù6H]Š-\Ì\÷\ãC‚z\0wS\ä\Ùû¬ý%\Ð}ý?\"(°`\Ú°Ä´Da\ã\Å!}\r\Ú	2>\ì\Ðw¦\É\è6Ÿ`€_\ì¶ \Èd²\0Y€,@\Ì4ú;’c\É\Ä\ð&Ì‡;Á!¸²\àEž>–û\ôqR6UÁ¹\Ú	†\Ü/\è\÷°„\î\Â\ñ\ö—¿*°»}~=d\ßM\Îvþ²\Ç\ð\ë/\ã²d™¶\Í\Ó\ÔL‡ŒO\íˆ5KN/ý+lZ£\ï\Ù\ßìš‰©\Ç\÷€Tƒ\Ø\0L0t¢‹\æ„0\áN¯(\Ò\'\ô%}>ODqŠ\Äb„&Œ&H¢b«—³\ámÆ‡\÷\ó\õ\æ\r\ï3CrQH}\Ó\ÉÌƒŸŽ}“Á‹st‚± Aƒ¯O\èAû3¾NxŸnq\ö@\Ê\äƒ\öCÈ†¼\É\ÓA\òŠý\ö\Ã8A+\Æ\é\\\÷ù\ÚC!L’f\íLÚ°y\ñ@ƒ\ögR\×\Î*NUªj™3Þä¨š.\ó…7¨>\Æ\Ä@\õ\ñO½5\ÐPžUÃ°‹ec7A6’p°\0×¯xþˆ=\Ø|\óf¯\æ¹æ„˜\Ê!X&N\ßf¦È—…£\ZLË¶7!\Ñ$$\ç\ãS²q,\æ\Ô-«a©>(\ñÌŒ\ô\É\ä I³\ÅA\n\Ä\0–¾\á‡=\äJOLL¶G Xw\â,(<\áÿÞ‘‰\çD=\äk~¤\Û\í‡84N\Ü\Ì²\0Y€,@ È‚KbA±ÿ^W\'¶*\ÃJ`\Ü\Ë0\ò>>W”\0:pF¢!7\ç&>sª~L£¼ü´„\ô¤„\ö—=v*\Ü}\ÎpúcaˆÃš  \r\×\æx\ê \Ü\Ç5µn\ïMg­\Ýsd\ÓY+gm\Z®z\çØ¦³U‡î›ˆƒ›5ÝžbQ“Áz‹e!Ù¨\Ó[L\âcž\â¦\Ï\ò<\'\â˜\nQDø\é	cv\Þ\óœ\']\éM\Åú\à#?\\\íœ}Æ¼\ò£0Ok­ýr\Í/…\Ù\Î\åýR«uK\Êm³V]mtjuFf\àG\ß\\¢\áÙ¦*_\Õ>X\ÔK¨—ú\ê%86\ö?.â¤ \Îz˜ÿºoZØ‹«½\Ù\Þ)\ÊX[q\Ù?˜²¬)}€	\ã\Ê\Íf©&iHP„ž`\ë’n¡‡\Ð7“\Ð„\î\'\ËAÁ,\äÀ\ë±\Û_†\\bŠ–MùJ¦\Æ\0âžŒŽQ¾ŒkI\Ò-\Ó3Oys\Ä\õ\á:Ÿ¢5ùø‰œ)9¢\àxª) 1†\Za¬4\Â\ØÊ§7a³\è\Ó!Œ,Qæ±¯\ÑaGU<‰˜—´X±ƒ\ØÉ‰oÀh\Ô|3jÁj$\Û\ôDYB\Ô j\Æ5\ÏNB\Í #^\Ì3@N»e\ß\ÒLÅ–FÞ»8¨jªeXŽ“YN+\èŠ\á\n\ÖQ{OgÁq¨\öü<žA:Z5CP\å“–yžÀþŒÃ—\Õ\ÖoÞ…¼A\ç\ã¥)d˜\Ïÿ?7›o&€5Ž“ƒS0\÷ù±Äec¯\è;8rj\ôK§ª\âµ«%»–,©z6øf	Žix<ˆhB4M\Æ~ZŒa\00jI#†£\ÚÙ³\ëUrEG€\á\0ÀE\0\à›‚± Î³½y¥s\Â`\ÔhË†hŠ0\âwÁ€h®­;&\Â\0ap10`ŽLAœ?	p‰\r¼:»7#zDw5\ó”\ÙÄ±\ñfTxš\ëe&I$Cˆ dˆ;\ÄÝ¸ûªý¯\r¸»…ÀAL\Ø\írH\ß0?fv=\óMEŸs×¥«6\Å0\'g‡y8C³³­œý\à¨\Å[c ‹N\×i\ðˆžÐ—\Ãhº‘O.D³%’™\\’5O\ÐT3³‡ˆ\ë\Ó$h\ÐYš”±\Ç\Õ\"Š¦J†’Qª\'Èº©‚†Bd 2¦\ß’%]’m\Çë…hKžn\Û\è\n!F¬ F\ï#\Å1<O™˜O¶5Q\Ì\×\';¬m¢9S\0‰€w\ò}‹§¤ø)\Ït\Î0ªkÔ¾D89“lW\ñD\Å\ÔD\ôm)3\ëÛˆ†F4’UyŠmiŽ#\ã<\'\"c6|E5t¢p©\ê\ömdKÐ´ØŠC &Ù·‘t];ã½­o#iDV-#k±	®®ºy1z\éiÿi\Z\Ø\Í\öŸ<\ã\Ù~²®\r¶”\ò„Á:~f|\Ø\ÝC>™\Ãs\ö\í¶7\é{˜!j?¢?u¢û…O>úp7j§H°dAq\ä\ìñ©ž§X\ß\'CˆÍ¤S$y²\Æ`¢A;Ö \àhDuD\"c&œ\"Y0\ÉU39©ˆî™¢n\á¼\'\Â`\â\"\Å\Ô,\ÇT!E\ÒD8E¦,ZH·^r\ÉSu\ð\ì\È\ó\ë¥g|I\Ü&Ÿ\Ý9rˆ\è\ët­\ÝWˆ\Ï\Å\é? \Ó\ÎN:G”œ#2–\ó@‚&\Ïu2«¹AU\r¥ ÐŒ¹<šk«ž\Ì#k]\ÈL\Õ#\n®·FdÌˆ\Ë#‰– Yª\ÓUvm‰\ð³zƒ‰vyDCUlE˜”}@šä‰‚Â£\r\Ý›¬Ú¢E¸\Ô# \ç\ÖK\Ýk\Ü`’m\ê\ò~\Þ\ò}@\ÇÓ‰‚#D“ƒ%»Ð·\Ã(·‘{?‚¦J:`wc‰(†faN\Ä\Ò\ìz?\nQ=8™H·\ìxŠ\äx¸µ‘1Þhz¦\î™\ÙE7²¢Iª‚\ñe„Á\Ä{?Ä²mS\â§O‚\÷Ã€§Ù–š±\Ø$ÁvlW\â{  \ç\×K|\í\ä\ï…n½\ë\à9>t;ž\ì¡oÁu*¾\Êü ú–ùE½®\æTq#\Ïr@tI#$c\é©DµU\ÅB‡ˆš]H³\\Yu3ºF“t]vŒ´!2f\Ã’K’Ln\\u‡<\Ñ%\Z\ß&‡0@L´¤‰†\ã:R\Æ\Ë\ß Mt•›…=QkGc¯µH\äù\õÒ‹~>$yÛ†›\×0!4Ï³\ì\ò,p?Â¾ 8Ÿ\Ûnœá¾\á\Õ\÷\ÙßŒ5Œžµ#D<]%º™1\÷DGr×…\Ùa„\Âj&!Ywˆad‘!›\Z!²„[O³\á)DqlAÈ¦{\Ó\\Y4²Gÿ ­ F\ï©–¬8²<)»ˆm8že&\èlÇ“-\Ñ\Ô1A/\ò‚\ô\Òwt\'N\äv|\"ˆ;F\ïX\É6¸G\Ã(­‘\Û#Ù–`\ð½pÝ¶›kx¦¦C¦\Äbd&½\ZÅ“L]²[\ß\×R~¢0\"‘qq^M\Æ\õ}k\ì17üF\Åý\Ê\õÒªo…~\é¯-«[¦W3	\Éh8b\êžo“@#ŽG¥\áNL~‡\r.Ëµ\ã¢-‰Š­\ë˜i\'øc±hŸû°\á¤E{4¢\÷û1\ó\\\ñT™È™\Ý\\\Ü\ÃWÙ——\Óe¢¤˜\Z9m¿\à¸u™¤\ÎD—mLÿY\ßNþ\Ýj\ß\ç3³\í‡0E\Û~\0\ñ	Xº\Ý9i+kƒN0«\ÖÓ‚“øšþ•–“\Ï=,ˆÁ¦\éR6d\02\0€˜jT&…\Î\",ˆdaÞ˜8†\å\â\Íˆ<Eª\òVˆ\0}\Ó\Ûÿý­bÁsWR2\ÛH\Ð*F«ø’@K_\ò\é¹=H@\Ñ1aK\Ö{¾<qŸœ4Š©®Ltwº’¼/ÅŒ\÷²\õNQ\Î\î°65\n\rM d\02\à<\Èa‹\'\rº \é¦<\õ¼Z:‘	3\"0K‚š\ÇJ‹0®6%\\\É\ë7N\rFr6X™n0Œ\Â\Ä\Ä\0B±ÿ´š¥¹šdf\æºU]•L\×Æ™Ð«\éW\èª	 ˜V{	\'›\ñ\Ñ\Ú\÷q\r8\Õ_\Ñ#\Èd²\0Y€,˜\\\ä\óüŠ\':~G‹¤§¹\ËO	\Òo™\Ñø\Z\0Â®±}¾@\÷:B³\'(ý]?\Å!:\ÑTH+=‹`«\r`i\Í_‰€]\ßÇ´R\r[Ñ‡¼¦&$,<Z½Dkq\Ù%t|5w\÷\Ë}º?)»í‡‘Y«®6:øYoúa«V›Q^\÷rløHù}\Ïsì¼‡´Û~9N#\Æ81j|.r¹‚\\™*®\ð’—±!ø\Ïp’M²\õn\õ\Èý\r\ZU\×l\Ë\"™}*1-\Í\áŽ1–}ù\Ö\è˜W\Ë~\Ñþ”\'\ð{\Í\rŒ]\ÈNNßµaT»ƒ{d²\0Y€,@ 0¤›´˜™—\Ò¶g»\ÛC¿§»üKn\ò´7Ù•Ÿ[ù\ã°\ÜQ&²\èÉ™L*‡\Å8\ìŒ\ñ\ã°ù…Q$\ä\nr¹2ŽqXYwD\ÇÊž”\Ò× ‘Tµ;[\\\ÌýŒ•\Óe\Ð\ôþ¼Û ‰ùâ—£ë®<>\ñÕ›À]H˜\'\Zqú\É5v¯\êRb£4W?*\Å(h\Âo’\Ã.««k\ì}\ôø&f¼DAý\è\Û\Ø\ðµ\Ø&[\óK0À\êaW‚€[R\É\Ç\Õ\õ(1¬ø\Ó\ÊA\r:6‰!v¥JPN\äÌ­\ëÕ¨¼o¢Žû.n6¿]*wù\r«²^\÷\Ñ\Òÿ\0\0ÿÿ\0PK\0\0\0\0\0!\0\Öd³Q\ô\0\0\01\0\0\0word/_rels/document.xml.rels ¢( \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0¬’\Ëj\Ã0E\÷…þƒ˜}-;}PB\älJ!\Û\Öý\0E?¨,	\Í\ôá¿¯HI\ë\Ð`º\ðr®˜sÏ€6\Û\ÏÁŠwŒ\Ô{§ \ÈrèŒ¯{\×*x©¯\îAkWk\ë*‘`[^^lž\ÐjNK\Ô\õD¢8R\Ð1‡µ”d:4e> K/ƒ\æ4\ÆVm^u‹r•\çw2NPž0Å®Vw\õ5ˆjø¶oš\Þ\àƒ7o:>S!?pÿŒ\Ì\é8JX[d“0KD\çEVKŠ\Ð‹c2§P,ªÀ£Å©Àaž«¿]²ž\Ó.þ¶\Æï°˜s¸YÒ¡\ñŽ+½·Ÿ\è(!O>zù\0\0ÿÿ\0PK\0\0\0\0\0!\0¥^}-$\0\0\×\0\0\0\0\0word/theme/theme1.xml\ìY\ÍnE¿#\ñ£½·¶;M¢:U\ì\Ø-´i£$-\êq¼;Þfvg53N\ê[•‘@ˆ‚8P	¸p@@¤qi\ßÁ}†B©¯Àfw\í{B\Ý&ˆ\n\êƒw>~ÿï±\Ï_¸3´O„¤<izµ³U‘\Ä\çMÂ¦w}·{f\ÙCR\á$ÀŒ\'¤\é\r‰\ô.¬½û\Îy¼ª\"\ô‰\\\ÅM/R*]­T¤\ËXž\å)I`¯\ÏEŒLEX	>\0¾1«,T«K•\Ó\ÄC	Ž\í\è›\ÑO£G£#t­ß§>\ñ\Ö\nþ_‰’zÁgbGs\'\Ñ\×OGG£Ç£‡££\'w`üž\Ú`¯¦r(\ÛL }ÌšˆøÁ.¹­<Ä°T°\Ñ\ôª\æ\ãU\Ö\ÎW\ÆDLC[¢\ëšON—{†N„½1a­[_9·1\æo\0L\Í\â:N»S\ó3\0\ìû`y¦K[\ï.\×Z\Ï(\Î\ònWÕº/\ñ_œÁ¯´Z­ÆŠ…7 lXŸÁ/W—\ê\ëÞ€²acVÿ\Öz»½d\á\r(.\Í\à»\çV–\ê6Þ€\"F“½´Ž\ç82cHŸ³KNø2À—‹˜ *¥l\Ë\è5o\î\Åø] 0ÁÆŠ&H\rS\Ò\Ç>Ðµq\Ükx•\à\ÒN¶\äË™%-I_\ÐT5½\÷SE3¼x\ôý‹G\Ð\ÓÃ‡O~z\÷\î\Ó\ÃT—p–©žûÉŸ\÷\ï ?|\õü\Þgn¼,\ãý\á\Ã_\êª2\ð\Ù\çG¿=<z\ö\ÅG¿w\Ï_¸W†\ïÒ˜Ht• mƒa¤\'^b7Â´L±ž„\'X\Ó8\ÐY\è«C\Ì\ò\èX¸±=xC@Kp/nY\n\ïDb ¨x9Š-\à&\ç¬Å…Ó¦\ËZV\Ùƒ$tƒ2n\ã}—\ì\öT|;ƒr»HK\ZK\Í-!\Ç!IˆBz\ï\â »I©\å\×M\ê.y_¡›µ0uºd—\ö¬lš]¢1\Äe\èR\âmùf\ójq\æb¿A\öm$Tf.–„Yn¼ˆ\n\ÇNq\Ì\Ê\È+XE.%w†Â·.D:$Œ£N@¤t\Ñ\\CK\Ý\Ëz“3\ì›l\ÛH¡\èžys^Fn\ð½v„\ãÔ©3M¢2\ö=¹)Š\ÑWN%¸]!zqÀÉ±\á¾A‰\î—\×\öu\ZZ*MD\ï„«$·\ëq\Èú˜æ•©^\Ó\ä\ï\Z7£Ð¹3	§×¸¡U>ûò¾»³¾‘-{\Þ^®š™n\Ô\Ç\á¦\Ûs›‹€¾ù\Ýy’-á€¾m\Îo›\ó¾9WÏ§ß’\']\ØÉ‹ƒ·a\Ï}\n\ïS\ÆvÔ‘+\Ò\ôs	\æ]X4\Ãd|	H#\æ\â-\\(°#Á\ÕTE;NAl\ÍHe\Î:”(\å®f\Ù\É[oÀûDek\â\Ò	h¬6y-/–/£c6fšp!hQ3˜W\Øâ¹“	«eÀ9¥ÕŒj³\Ò\Æ&;¥™G\îM¨#„\õ¯µ¥…L4$f$\Ð~\Ïa9\õ\É$‘¶{Öš\ñ\Ûn\Ó\Ëù¥­h¶\'6O\Ê\â\êÇˆ+¢w’(&Q\Òu<UŽ,±g\è\0´j,4<\ä\ã´\é\õ\áø\Ã8~R·.\ÌÂ¤\éù*7\å¥\Å<m°;-k\Õc\r¶D¤Bª\r,£Œ\Êl\åD,™\è¿Ð¨k?œŽŽn4Ÿ‹ËµQ\ó(‡–\ôû\ÄWÇ¬L¦ù(\"v¢\à\0\õ\Ø@lc\Ð[§*\ØP	¯“kz\" B\Í\Ì\ì\ÊÏ«`ú7¡¼:0K#œ\÷$]¢……ÜŒ\Ç:˜YI½\ñlJ\÷\×4Å”ü)™RN\ãÿ™):s\áÀ»\è¡\Ç‘\ÎÑ¦Ç…Š8t¡4¢~WÀA\Â\È½”…V	1ý£·Ö•\ìOúV\Æ\Ãœ`\Ô6\r‘ \Ð\éT$\ÙR¹/aVË»b^9£¼ÏŒÕ•i\ö\ì‘}\Âvu\õ.iû=\Ý$w„ÁMÍž\ç\Îè…ºP\ßÔ“O–6¯z<˜\Ê\è\çVjú¥WÁ\Ê\ÉTx\ÅWmÖ±f\Ä-4\æ~Õ¦pmAú\Z7>\Ëþ\Ñ/\Ô]¾\r\ÑG¬8Q\"H\Ä3\ÙÁ\éR\ÌF=\Ð9[Ì¤iV™„\ê5	ÁXî”³\Ë\ÅqŠ\Î—¦œý\÷\â^\ß\Ùù\È\òu9®®Ì–h¥t±1³™¾x\ï\ÈÞ€ûÒ€)i\ì#·\á’\Ú.þ£\0>™DCº\ö\0\0\0ÿÿ\0PK\0\0\0\0\0!\0QQe\ì\Ï\0\0\Ô\0\0\0\0\0word/settings.xml´W\ßo\â8~?\éþ\Ä\óQ\ò;!·tU \\»*·§¥«{6‰«v\Ù”]\Ýÿ~c\'\ÚF«²«¾€™o\æ›\ñx<>||b´·\ÃB^Žû\î•\Ó\ï\á2\ç)7\ãþ×‡ù \é\÷¤Be(/\ñ¸À²ÿ\ñú\÷\ß>\ìS‰•5\ÙŠR¦,\÷·JU\ép(\ó-fH^\ñ\n—\0®¹`HÁO±2$\ëjsV!EV„uzŽ\õ[\Z>\î×¢L[Š#¹\à’¯•6IùzMr\Ü~Y\ñ¿ÉŒ\ç5Ã¥2‡Sˆ—rK*i\Ù\ØÏ²¸µ$»mbÇ¨\ÕÛ»\Î¶»\ç¢8Z¼%<mP	žc)\á€µ’\ò\ä8xEt\ô}¾\Û-\Z*0w³:<¼ŒÀ{E\åø\é2Ž¤\å‚\å9).ã‰Ž<\ä”X7ú¹`\ÎŠú\"\nÏ·q\è/m~\Æ%Ul/£³g4Ô¶H¡-’ÇŠl\×\ô2\Æ\àŒ±)0\Ê\ó\ÇsN|Y\Ò\Â#á\ÎP¾«£ªèž¬M\ÏhKš\å\éÝ¦\ä­(„¥Ýƒ\ê\ì™\è\ô\'²þ2Küd\ä:·\íbM\õR\r-\íç¬·O+,r¸\×\Ð§?\Ô\0\Ü&¾^*¤€1•¦\Ô4Èœb\ìÓ@Z›•›¯QM\ÕZ-¯@i‡`Ÿ±“4p¾E\å\n‹e…r`›\òR	N­^Áÿ\æj\nmRÀ-n-L\Ó<­–M‹1\Øù³¦º\àÖ‘Õ‚¼ýˆ´\ñ\î†\ç._:\â\ð`R\à\ñ¥:P<‡\à—\ä¾)‹OµTMký…~\0.µ\ç\ÏP#‡\n\Ï1R5¤éœ™“˜SR-ˆ\\Ü•\ÔÆ»9#\ë5\à€@­- |ˆ\à{“\ç[Œ\nx§\ß\Éo-\ñ¿ W\Ô€²|œp¥8»=T[\È\õ¯¤¹B\Ã\ó\ò…i£v\ñ…suTuœ8Îœ ‰T£oBnb\Ö\î\î2³À\ëB<\'¼™w\ÚxQ;\Ý\È\Ä\óFmCx‰Ä‰ß‰øQN²Nd\âùÙ¨	ƒ8œvF\Î\ã™\ß[\äûqu\"¤3‚8q\æIg\Ô\ñ\È%q\'’Es·3‚\Ä\ñ“›\Î\óI\\\×uÆ–DþlÒ¶š\ç\È(\ñ\÷¦™À\éÄ6“©\ã;N\Ãi6\éD2\×	;s¹Qu\î\'\ó\Ý\ð\Æ\ìgx¬e–\êù\ïaWº!\öXc1El%\ê-\ô„8\Ô\Z+\ñ8!¥\ÅWž9|Ž,\ë•ƒQ:‡«isp,-ˆ¬fxm\Öt\Ä\æ\Ä\ÛjˆN)¼NŸŽ\\úµ\Ã\â/Á\ëªA\÷UM£³*n´–¤T\÷„Y¹¬WKkU\Â\Ã|\Õe\ñy\'LžN\éÙ§\n\Z‡y0\î‘i@FWÔƒ/_›d\çT,usÁTUMZm\ÜqŸ’\ÍV¹º­(øUÀ	\ócµ\ñZ\Ì3˜\×`\æ\Ê\õ\Î@»]œdž•\éùV\æŸd•\'Yhe\áIYY¤e[x•Œ\Ð.\íR\Ë×œR¾\Ç\Å\í	%j’ ·¨Â³f‚€\òâ )do—\â\'˜OpAü?«HÁÐ“W<S–­6E^«gº\Z\Ó\Ê\Õs=-¶\Ä\ð™±)\ñ±\è\É&\'PŽ\Ë[–?šÀ)‘\ð¸T0\Û(.,\ö§Á\Ü -x~§§± ‘\Ù\Ä&£¦º\áø{\Î\Ü r\ÃA\â†\ñ e\ÓÁh2s®=\0¡\ï»ÿµ\Ñþ½þ\0\0ÿÿ\0PK\0\0\0\0\0!\0Ó¹Á¹Ÿ\0\0Oy\0\0\0\0\0word/styles.xml\ì\Ír\Û\È\Ç\ï©\Ê; xJ2\õ-Ûµ\Ú-I¶#\ÕZ¶Ö”\Ö\ç!0\'0>,i9ä’§\Èl©J%/!¿Qf\09Tc@\ô £Kr‘Hý\Ã\Ìü»{¦\ñA|\÷\Ã}_y–™v^lž†2\é\í\ñ\è\æú\Ý\Ö\ËQ,X,S~<z\àù\è‡\ïû›\ï\î^\ç\ÅC\Ì\ó@\Òüu\æE±x=\ç\áœ\',!<U\Îd–°B½\Ín\Ç	Ë¾”‹­P&Vˆ©ˆE\ñ0\Þ\Ý\Þ>Õ˜¬E\Îf\"\äodX&<-Œý8\ã±\"\Ê4Ÿ‹E\Þ\Ð\îú\Ð\îd-2\ò<WNâŠ—0‘.1;û\0”ˆ0“¹œ/Tg\ê”2\ß\Ù6¯’x8Àv\à0\ä\÷8\ÆËš1V–6GD8\Î\á’#\"‹\ã\×•(\Ä\î^\ÓýO›[¬<*¢9\×h4Ö¶¬`s–\Ï×‰³GÜ·ˆ•ƒ\Å2üb39n\Ð–À‡Dk˜„¯/nS™±i¬H\Ê+\åX\ë¿JýÏ¼\ä\÷f»–ú\Å,\Ö/Ô¨}¯B7’\á>ce\\\äúmv•\Õo\ëw\æ\ß;™yp\÷š\å¡×ª½j§‰Pû??Is1RŸp–\'¹`­\Î\õ‹\ÖOÂ¼°6ŸŠHŒ\Æzù/\êÃ¯L\rû\în³\åL·`m[\Ì\Ò\Ûf[Vn}º±[r<\â\é\Ö\ÍDoš*\î\ñˆe[“m8®;Vý·º»xú\Î\ìxÁBa\ö\ÃfWYI%\r…N‚»G‡Í›O¥Ö‚•…¬wb\0\Õÿ%vF\\%+•º&UUŸ\ò\Ù{\å+<š\êƒ\ã‘Ù—\Úxsq•	™©,y<z\õª\Þ8\á‰8Q\ÄS\ë‹\é\\Dü\óœ§79V\Ûzg±\Þ\Ê2U¯\÷T\óM#\ò\è\í}\È:oªOS¦5ù \rbý\íR¬vn\Ìÿ\ÔÀvj%\Ú\ì\çœ\é\É#\ØyŠ0\ÍG!vµEn\õ¶Y>\é»ùjG{Ïµ£ý\ç\Ú\ÑÁs\í\È\Âs\ì\è\è¹v\ô\ò¹vd0ÿ\Í‰4R\ó€ù>\Ü\r n\â8¢\Íqš\ãˆ%4\Ç*hŽ#\Ð‡££9?FsnŠ\à2ty¡\å\ì{o\ï\ænž#ü¸›§?\î\æÀ»9\áûq7\çw?\î\æt\î\ÇÝœ½ý¸›“5ž[-µ‚fi18\ÊfR©,xP\ðû\á4–*–©¨ixz\Ò\ãI\'	0Uf«\'\âÁ´™\÷›=\Ä©ÿ|^\è\Â/³`&nËŒ\çƒ\ÎÓ¯<–°(R<B`Æ‹2sŒˆOg|\Æ3ž†œÒ±é º\Ò2™ø\æ‚Ý’±x\Z_C$I\nK‡V\õ\ó\\‰ pê„…™\Þ4\É\È\ò\Ã{‘+\r	N\Ë8\æD¬4.fX\Ãkƒ^\Z\Ì\ð\ÊÀ`†–fTCTÓˆFª¦\rXM#\Z·\Ê?©Æ­¦[M#\Z·š6|Ü®E›o¯:vú»;‹¥>2¸q›2µ\0>\Ý\Ô\ÇLƒ+–±ÛŒ-\æ>*ÝŽµûŒ\ÝÏ©Œ‚kŠ9mI¢Z\×9S½i9|@\×hTÁµ\ä…×’G`K\Þ\ð»T\Ëd½@;§©g&\å´h\rZC\ê´—Õ‚vx´±b¸‡­\à\Èr²0h\Çx\ð½œ\ÕrRd¾U+‡7l\Å\ZVO³i\ój$A+\õ	Sš4|þ°\à™*Ë¾&½“q,\ïxDGœ™¬|\Íù]#I¯›,\æ,¦VZC\ôŸê›«\'‚K¶Ü¡«˜‰”F··[	q@·‚8¿¾|\\Ë….3\õÀ\Ð\0OeQÈ„ŒY	ü\Ýg>ý=MOTœ>\õ\ö„\èð	‚I¦\"Éˆˆ¤–™\"$s¨\áý\È¦’e\r\í*\ã\Õ\õ$\'\"NX²¨±¥\ò\â\Ê?«!\Ãû™eB¢\nªk˜u\Ø0/§\ä\á\ðT\÷A$G†>–…9þh–ºÆš7|™°†¾D0jª\éAû/Ag\×p\Ã;»†£\ê\ìY\Ì\ò\\8O¡z\ó¨º\Û\ð¨û;¼ø«y2–Ù¬Œ\é°’`$B—IšS\ö\Ø\ð;lx\Ôý%t\Ã#8$gx\ÈDD&†Q)a`T2•F*À\ð+t,\Ø\ð\Ët,\Ø\ðku*\ÑÀ‚Qù\é\ôOt–Ç‚Qù™Qù™Qù™Qù\ÙÞ›€\ÏfjL7\ÅXH*Ÿ³tMZ\ðd!3–=!\ß\Æü– ­hW™œ\é;YdZ]\ÄM€\ÔÇ¨c\Â\Åv…£ù3Ÿ’5M³(\ÛEpD”Å±”D\Ç\ÖVŽ±´¼\Úhf\î\äÜ„«˜…|.\ãˆgŽ>¹mU½<©n\Ëx\Ú|ÓŒ^‡=ß‹\ÛyL\æË£ý6\æp{£eS°¯™m\ÞaÛ˜6\÷³´™]\òH”I\ÓPx3\Å\á^c\ã\Ñk\Æû›W+‰5Ëƒž–pŸ‡›-W«\ä5Ë£ž–pŸ/{Zš8]³ìŠ‡7,û\Ò\êG]þ³¬\ñ\Îw\Ô\åEK\ã\Ö\Ýv9\ÒÒ²\Íº¼h-T‚“0\Ôg :ýb\Æm\ß/x\Ü\ö˜(rS0\á\ä¦\ôŽ+7¢+À>\ñ¯B\Ïì˜¤i\ö·¼z\â\é\î\ö\Ì\"ºW\æü©”\ÕqûµNýo\êºP§4\çA+g¯ÿ‰«µ,\ã\Ç\Þ\éÆ\èwÜˆ\Þ	Èè•‰œæ¨”\ä¦\ô\ÎMnD\ï$\åF ³œp\Ù\n\Ú\ã²´\÷\ÉVâ“­¬Üˆ\Þ\Ë7¨\Ô+7¨À\Ü+P!¨Tˆ@*\\€\á\Ú\ã\Úû*¤ø*¤ \"Ð\n\è@…t B:P=\×\öNs¯@…t B:P!¨f½8 P¡=.P¡½O BŠO B\n:P!¨Tˆ@*D \"P\nÌ½RÐ\n\è@…t V·\Zú*´\Ç*´\÷	TH\ñ	THA*D \"Ð\n\è@…t B*P¹W B\n:P!¨Ts²p@ B{\\ B{Ÿ@…Ÿ@…t B:P!¨Tˆ@*D ˜{*¤ \"Ð\n]þYŸ¢t]f¿ƒ?\ê\é¼b¿ÿ©«ºQŸ\ì[¹m\Ô^T\Ó*7«ÿ½§R~	Zo<\Ü3\õF?ˆ˜\ÆBšCÔŽ\Ó\ê6\×\\:\ñù\ñ¬û›>\ðG—\ê{!\Ì9S\0\ß\ïk	Ž©\ìw¹¼m	Š¼ý.O·-Áªs¿+ûÚ–`\Z\Ü\ïJº&.›‹R\ÔtŒ»ÒŒe¼\ã0\ï\ÊÖ–9\â®m\Â\î\ÊÌ–!\à®|l:9?µ>\è9N‡\Ë\ëK¡\Ë-Â‘›\Ð\å–P«&\ÃÀ\è+š›\ÐW=7¡¯ŒnJO\'/¬…VØ\ò“\Z†Vjÿ@u°RC‚—\Ô\0\ã/5DyK\rQ~R\ÃÄˆ•\Z°Rû\'g7ÁKj€\ñ—\Z¢¼¥†(?©\áT†•\Z°RCV\ê²\ã/5DyK\rQ~R\Ã\ÅVjHÀJ\r	X©!ÁKj€\ñ—\Z¢¼¥†(?©A•Œ–\Z°RCVjH\ð’\Z`ü¥†(o©!ªKjseMj”Â–9nf\â&d\Ë—œ-CjÉ²\ö¬–,‚gµµj4\ÇUK¶hnB_\õÜ„¾2º	(=¼°nZa7\ÊOj\\µ\Ô&µ º	X©qÕ’Sj\\µ\Ô)5®Z\ê”\ZW-¹¥\ÆUKmRãª¥6©ý“³›\à%5®Z\ê”\ZW-uJ«–\ÜRãª¥6©q\ÕR›Ô¸j©M\ê²\ã/5®Z\ê”\ZW-¹¥\ÆUKmRãª¥6©q\ÕR›Ô¸j\É)5®Z\ê”\ZW-uJ«–\ÜRãª¥6©q\ÕR›Ô¸j©Mj\\µ\ä”\ZW-uJ«–:¥\ÆUK—\ÊDü\Ô$aY\Ðý^\Ü9\Ë\çþ\ã„7i\Æs\åQ@\Û\Õ\÷¨^Ž\ï\Ö¥\Ù\æQ‚\êû…\Z3ý\è\Ö\íJQ\õ°5\Ð|\ñB‘˜y‚•nDP?¬~p•ik}¦Ö¼\ÎrUN\×\ß\Ù\Þ>{»³\Ý8A\ëƒÎŽGg,\Ól\ígkÍƒ\ÍÖ¶„ù\ñ\èZ$<>\ð»\à“LXZw´y\ä˜i7\ìi8W]\r\ëŸ\Îr\õtt\Õñ«¸¦S+oo¾]\ë·§úÞš4Uk­,ttuµp\Ç!F—®v½ªÍ¦†©fL\ãJ*\õ\â\"\Õj\ÞÕ$«\ZÝ³\n¥>?\ãq|ÉªoË…û«1ŸÕ§;\Û\ægž|>­~\á\ÏiŸ™©À	¯7¦z\Û\í\Õoþ\×\×(¸†z·e¨\Í\Å2CG¹‡ü«V\ìVTXºª‡)\ìG(\ÌÇ¬vBØ¾\æ\Ösw˜º\Ég?où¦ý|\ë>t*³ˆg&\óT>b\öªúº\î\è/j\Z4/\Ô>ù\ò\áyjnY‘—\äe»\ô./\ë\Æ\÷¼Œ…\Ê^?fþ³Ÿy\Ë\á\ïK\ï\Ë\\\r™™3žF\Ì?{üÇ·??þ\ë\ñ\×@ýû\õ\ñ\ïÿ~üç·¿|ûk\í‡\÷L\õ\Ï\Ù6\Û\ê\ëfúº\ì\î\é\î\î«z\Ñ\ó—ý_r\Ù\æUþý\0\0\0ÿÿ\0PK\0\0\0\0\0!\0¼[x\0\0;\0\0\0\0\0word/webSettings.xmlœ\Ó\Éj\Ã0\0\Ð{¡ÿ`|O\ä¤I(!”’R\è]\îŠ<ŽE$‘”:\î\×w\ä,u\È%\îÅš‘<­“ùV«\è¬“h¦q¯›\Ä©4«iüù±\è\ÜÆ‘\óÜ¤\\¡i\\‹\ç³\ë«I9.aù\ÞÓŸ.\"Å¸±\Ó8\÷¾3\æDš».`h0C«¹§Ô®˜\æv½):uÁ½\\J%}\ÅúI2Š\÷Œ½DÁ,“\îQl4_\×3ŠD4.—…;h\å%Z‰6-,\npŽÖ£\Õ\Î\Ó\\š#\ÓœAZ\n‹3ß¥\Å\ìgTST\ÞK\êH«?`\Ø\èŸ#\Ûv\Æ\í\Þ`T\Ùtd\Ú\Î™6œÿM¦¤›VDÿ\æ0Ð„\ò†\åRŸ\æ\í¸\Ã±P\Ë=Ï¹\ËO\ÅLµ\rqwÁŠuÓ„v›6<‚•g¨\Åøqe\Ð\ò¥\"‰neD+ª\á\ð¥\ó	MÂ¶\îÛ²2Úµ½_,¼\Ô\òh\ï,–,\Ý\ôˆªW\ó\õüTg\\),\ß^(a\'O~\ö\0\0ÿÿ\0PK\0\0\0\0\0!\0Ê„5¥$\0\0#\0\0\0\0\0word/fontTable.xml¼“\Ín£0€\ï+\õ\÷CHšFM*5\ÛH{\ÙÃª}\0Ç˜`\Õ?\È\ã„\ä\íwleu·\ô°9€™\ñ|\ñ|\'%£#· Œ^\Å\é„\Ä\×\ÌB\ïW\ñ\ë\Ë\övG\à¨.¨4š¯\â3‡øq}\ó\í¡Y–F;ˆ°^\ÃR±U\\9W/“X\Å…‰©¹\Ædi¬¢\í>QÔ¾\ê[fTM\Ø	)\Ü9\É™\Ç\Æ~†b\ÊR0þÝ°ƒ\âÚ…ú\Är‰D£¡5\\h\Ígh±Em\r\ã\0Ø³’-OQ¡{Lš_”`Ö€)\Ý›\éNPXž’°R\ò0È®\0s\ÆO\ã‹Ž‘`\å#Šqœy\ÏÅ€\óµ\Ã\0\Åa\"›^\Î\áo¾|À‚\Â\Õ8\Ü\å%¾–:ZQ¨þ$–r1\Û“†½\r™|œ´Y<+ÿ[þ\Økc\éN\"	§2\ÂÁŠ\Ø_\ñýø[X\òSˆ{-Ý¢”~\Ö\ÖÝ—5KM‚6TŠ!QSm€§˜;Rl5mÉŒx]\É\É\Ô_\ã\ÄodµÀ=$l\Ül\ÚpI•\çK\Z\Ð&j\áXu‰©¾‰6b‰\ì\È*~\Î	Éž·Û¸¤H&\ÉïžºH†‡j\÷]d\ÚGˆ°À	i\Ëa\Ó\ïÁÿLZW&^„\âý\äM\ô\Ë(ª?0’‘9š˜¡of:Êˆ\r\ÜQF|ÿWF\î³ÿbdCŽýÀ„7Ðš\ðF\Æ\Í\Æ\×Lù\ÐDžù\Ù\è#\ÞD\ö\Þ\÷\ßM\Üÿ\ËD·€\õo\0\0\0ÿÿ\0PK\0\0\0\0\0!\0+7[¤\0\0\0\0\0docProps/core.xml ¢( \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0œ’\ÍN\ã0\Ç\ïHû‘ï©“V ˆ\Ò -ˆ\Ó\"!Q\âf\ì¡x›8–m½\'Žp\å)ª•V\âRžÁ}#&I›\Ò§•™Ÿÿ\ÏLº_\äÁ+K5$q/\"(^\n©\ÆCr6:\nwI`S‚å¥‚!™‚%ûÙ­”ë„—NL©Á8	6@%e®‡\ä\Æ9Pjù\r\Ì\öP˜¼.MÁºfL5\ã6Ú¢Z€c‚9FkÁPwŠd))x\'©oM\ÞN!‡”³4\î\Åt\Í:0…ý\öB“ùB\ÒM5|‹®’}oeVUÕ«\rŠ\õ\Ç\ô\âø\×i\ó\ÔPªºWH–\nž8\ér\ÈRº6Ñ²·W¿»6\Ü9hsÌ•&\ó¯þ\ï\â\Ï\Ó\âÁ\Ï\Ï~\î?ü?üš\ó\Úx\ÃÈ¼&ü¿Oþ}\É`²‘]I\ÕCšÀ´*°ø\Ã\r1–©Ž¾-g#€tÎ¬;\Æ]¸– ~N³¸‘ø\'Xs\îd½@Y¿!:7]N£-D€]LÚž¯2çƒƒ\Ã\Ñ\ÉúQ;Œv\Âxo\Ç\Év”D\Ñe]\Ó\Æýµ`±,\à¿Wm[679û\0\0ÿÿ\0PK\0\0\0\0\0!\0ý¾Rv\0\0\É\0\0\0docProps/app.xml ¢( \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0œRMO\Ã0½#\ñª\ÞYº\rB^&´	q\àc\Ò\n;G©\ÛF¤I”dû\÷8”•\"n\äd?\Ç\Ï\ï9\åG§³ú ¬Y\ä\ÓI‘gh¤­”iùkyq“g!\nS	m\r.\ò#†|\É\Ï\Ï`\ã­C†Œ(LX\ämŒî–± [\ìD˜P\ÙP¥¶¾‘R\ß0[\×J\â\Ú\Ê}‡&²YQ\\3üˆh*¬.\Ü@˜\÷Œ·‡ø_\Ò\ÊÊ¤/¼•GG|J\ìœùs\ê\ÔÀ\0J….U‡¼ xH`#\Z|¬`g}Eù\ÕXÂª^\ÈH\Ë\ã\Ó\Ëù°\0w\Îi%E¤½\ò\'%½\r¶Ž\ÙË—\Ø,\0_2°E¹\÷*“q\nÊ‚)M\î#\Ò\æE\ã…kŸ\'C[)4®\È;¯…\ì€•\íœ0\ÄÇ†ˆø\ÞÃ«+\í:\í\â»\å78²¹S±\Ý:!“˜\ë›ù\Ø\ð¨[B±\"ƒ†€z¯\Ó\0\ê5\rV§;i…oýÏ¤q“‚\Î\×\ÎN¾ÿ\0\0ÿÿ\0PK-\0\0\0\0\0\0!\0ß¤\ÒlZ\0\0 \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0[Content_Types].xmlPK-\0\0\0\0\0\0!\0‘\Z·\ï\0\0\0N\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0“\0\0_rels/.relsPK-\0\0\0\0\0\0!\0qû°\ò\0\0\óU\0\0\0\0\0\0\0\0\0\0\0\0\0\0³\0\0word/document.xmlPK-\0\0\0\0\0\0!\0\Öd³Q\ô\0\0\01\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\Ô\0\0word/_rels/document.xml.relsPK-\0\0\0\0\0\0!\0¥^}-$\0\0\×\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\n\0\0word/theme/theme1.xmlPK-\0\0\0\0\0\0!\0QQe\ì\Ï\0\0\Ô\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0a$\0\0word/settings.xmlPK-\0\0\0\0\0\0!\0Ó¹Á¹Ÿ\0\0Oy\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0_)\0\0word/styles.xmlPK-\0\0\0\0\0\0!\0¼[x\0\0;\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0+6\0\0word/webSettings.xmlPK-\0\0\0\0\0\0!\0Ê„5¥$\0\0#\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\Õ7\0\0word/fontTable.xmlPK-\0\0\0\0\0\0!\0+7[¤\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0):\0\0docProps/core.xmlPK-\0\0\0\0\0\0!\0ý¾Rv\0\0\É\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0=\0\0docProps/app.xmlPK\0\0\0\0\0\0Á\0\0°?\0\0\0\0','2025-06-30 07:30:49'),(2,2,'21321321321',NULL,'2025-06-30 07:44:14'),(3,2,'123',_binary '‰PNG\r\n\Z\n\0\0\0\rIHDR\0\0’\0\0‚\0\0\0S¶#`\0\0\0sRGB\0®\Î\é\0\0\0gAMA\0\0±üa\0\0\0	pHYs\0\0\Ã\0\0\Ã\Ço¨d\0\0UIDATx^\í½}”dU}\ï\Ý\æf\Ý<+¹y’`L\â[b\âK¢#d%Hc4\×denxX\ñå’Š\÷\É\êp×	*H\"(-\ò\Ö\ÑøÒŒJ	œI‡ˆ€Mš4\n\èŒ30#\Ì@‡\ÖÁF$¨0\à~\öo¿œ\ó\Ûû\ì½Ï©>»º«º¾Ÿµ6Ug¿ü\ö>§Z\ë3¿]§jB€MÎ²XœK«\æÐ²¼(f\ç–¯^]šs•Ž\õ\Ü}\÷\Ý\â¾û\î<\òˆøÖ·¾%¾\ó\ïˆ\ï~\÷»â©§žGŽ\Ï<\óŒøÁ~`z\÷Ë¼\èLLŠ™C\æ°\êß‘ÿ\å„ê†›\ï}\ï{\æ\Ù`x\×i\ïO?ýt´\ì\Üq¹\êc\0\0\0\"¹\éYKs³A$iÜœ\"¹9\È-’\'¾s¯8\ê¤\ë£\å5§\í	\n%•°H\Ò\ë2!&Š2*¯Q\ì\ï‰\×û\çÆ‹7v¾\ã´OŽ\Û*Yz\Ý)15¥\Ë\ôÂŠª[Y˜.\ê\Ê\Ò=\Õ\Ê\èu‹v;\ÖRÆ^“\"4¯\"3\Ö\ß]k`\×m_\ë\Ø\Æ\×g\\XY\Ó\ò\Z@$\Ç\ÊJÎŠYV\æ\æFE$Ç“\Ü\"’G¿„$’J\\$K©:43)&&g\Ä\ðkTS‘¬\ëC‡$‘¼\ß!13	™#€€…\Â~z¢‘>\'_u+O\îX’¾jFt\ÞH\Ì\Ä:i®n\ÑbE,LK\Ñ\ëvYlM›±œ\ð\õ#H$å…„HŽ+#³µ=žB$/¾\ö±\ó¦‡Å›Î¾U\Õ\Ñ#S½\É¶¯:¥©H\Æ\åk\Øh\"‰Múhi\ìøŸ—84#&G\ìc`\Ü!i\n‰$—;eé˜…•2%ûO/\ÈhMa\óFcr\Üu\öº¡5‡¨žG›±%©¶1A¾n\ô:A$\Çˆ\äP3‘|Ë…·‹;\îB¼\çÒƒª\îü+–\Å\î©ú¶\ÉÊ±*»\å«\ÅJe-½º\ô8žÝ£~²\Î\Ëz\ê˜\éy]üu[x}ƒ>Qa$Á`X‰c(\ÛV‘<+\ê‘2xfË·V*\Ëy£1ø:M\Æ\Ð\ÌZg‰~‘±4ge\Í	YŒ\\Ÿq\Âfv!’\ã\nDr¨„Hs\ê.\õü\Ú}‡U!‰$¨ÞŠ\ä\Ë\Î\Øï”¦\"\énm{\"6\ß\ñ¶{¹lùÇ³|üX\÷›t$M\Æ\é\È:g|j^B\Ç,…–—HœVO\"\ÜÊd*R\Â\ÛÑ±,eH\ö±\Í\ÍÛ›ˆd<\É^*Ã˜A>¶/‘Œ_Ÿ\ñ¡¼I\Ð\Zˆd~\õ\É\ë¸v{›Žm\ÏB\ò\Ò\ìf–ó²Šª³š\ï\èc_Ë¾n–úk47\Ó)biQœq\åÎ‰%K\Å\è\ZHb“>\ÈH‚‘Gg\æ‚rf>û\"‘dc2¨©Î›\É\Ä:\riiM‰\ä\Z\Ç&®\Ï\Ø@\×Àˆ7D´\"™ŸA‰$e\"\òH!•t\ÌE\Ò>\çuÍ¶¶Q\É*©bDÎªýH\ÔtŸù7‘;NlÝ¼¾IŸH\æ±\Ñ\Z\0\Øh\Ò5»¨\'y‚XH`#‘Œ\Ì‹Y³N\É`t½\rD²ß±\É\ë3&pù‡H‚\Ö@$\ó3(‘Lž…\ä¥o‘Tmé»—ƒ\"Y‘3\ÞV>§mt•‰Tý>\éy\Ýþœ\ð\\.^½ºk›Kc“ù‚’g	\É	•©£LT!W¬\Þy®³ˆz\nV›73¹Nƒ\Zk\ç\rA\ñ\"\"\É\Ç\Ò\\¶¶›\É\í\æÆ½.I\Ð\Zˆd~r‹\ä`¾G2$[•™s·˜\í¶¶*±\ÏSz\ã\âRi\Û\Ò\ã¶µmQ2Z/\0\Ãe“\ì\Í&•›N‚\ò\Ä\äNJ\é2\ã\ÏSbfb\r\å\Øä¼˜\ñþ³¬K»¦>‘±E2T7^\ð\ëG\"	Z‘\ÌOn‘\ô!9Ic¨„E\0\0À8\âü£B‘­H\æ\"	\0\0`H‚\ì@$\ó3h‘œÛ¹C	b“B}\0\0€I\Ð\Zˆd~-’\0\0\0@ ’ 5}‹$\Ýao¶\à\Ï7\0\õE\Ú\ê	º‘‚Ý¤!K\ì\î\Û\òŽ\ãÁ‘\0\00\n@$AkÖ’‘\ä?—·awº:\ëß‘k\Ä2¸¸Á\é4D\0\0À(\0‘­Õ­mý}„\Ö_\í¢¾J&\ò\å\Ò\ôµ/4`ˆ$\0\0€Q\0\"	Z3±\åtqƒ\É\í\â\ÍÇŠso\óE\ò\Z&i®°\éÌ¤Ÿ\Ý\Ó_LÍ·™‹/~\ö¾\'°t9“A\ô¶\É\Ã\ñ	?«I³½\ó-Å‘\Ç\ð–<D\0\0À(\0‘­\Ù:±Ut\×$’ò¹”¹É \è¾\ÜiY,\äQI¥wÒ‘C)‚X|\ê\ïÿ*‰\ß/!’•\ñy´H6¹k{i\ß-¦7\0\0\0\"	Z³u›\Ý\Ú&‘,³…TN¹:.’t\ÓJg>$p¯-°Õ¬c¨gº\ï\Ûr–\ò§~J/\ßÁ\Ð:ü¬%\'\ÕÖžA‹$‰b\è;#mL\0\0hD´\æ\ô-[Ä™72’W\"&Ž¿P\Ü\Éy)…:\Õ=\Âkk\"’‡H\ðtŸù\Ç\âS}H\æ+\ñ\Ç\çeDr\ï\Þ=I\0\0\0I ’ 5§o™\'uûI\ÊV\ò\ã\è~›kŽ®\è•}\õM43¢“U?£X3\×&ûŒdH\î\Üq¹\êc\0\0\0\"	Z3±u[dkûxq\á]¡­mþ=Œ1\Ñ#mJmü˜r	ŒÇ¯Þµ\Í\×\î\ñE’Ž\Ë\ÌOn‘<\ñ{\ÅQ\']-¯9mOP(©¤ERŽ´¸nƒ’k\õº‡_\Ç\á þw6ük\ãH¯;%¦¦t™6¿w·²0]Ô•¥+zª•\Ñ\ë\ív¬¥Œ\ëþŒž%4¯\"3\Ö\ß]k`\×m_\ë\Ø\Æ\×g\\XY\Ó\ò\Z@$AkF\ö—mÖœU\ì\ç#‰\Ü\"’G¿„$’JT$\Ô;>-\ëf²øuB\ÌZ1jq\0R\0\nû\éU~;\ÙB\âä‹¢\îo\å\ÉK\ÒW\íÏˆ\Î‰™X\'\Í\Õ-\ÚB¬ˆ…i)z\Ý.‹­i3–¾>c‰¤¼IÐšQþ‰D\õ\õ@}f\és™ƒ\ÌFƒÉ‹¯}@\ì¼\éa\ñ¦³oUu\ôH\ÇToE\ò„\í«N‰‹¤\ÎD\î2@$XHšB\"\É\åŽAY:fa¥L\Éþ\Ó2ZSØ¼Ñ˜w½nh\Í!ª\ç\ÑflIªmL¯½NIÐšQ\Éae\"ù–ow\Üÿ„xÏ¥U\ÝùW,‹\ÝS\õ}g$U62u³‘«N‡¾\Ç\Ó\ô3L½\r^ŽUbnë•™\Ò\ØP‰Z@`ù\Ç\"shBq%\×eq·\óu“Y\ÝDf\ê\Ã\ß0\Ï\é\Û*ý$l-\éohrm\ë,b\Ö\ÆÎ\Æ\è\ïb\ÕÇ±µV¯5\â\ÂÊ¶U$\ÏJ z¤ž\Ù\ò­•\Êr\ÞhL¾N“14s…\ÖY\âŸ_d,\ÍYYsB#\×gœ°™]ˆ$h\rD2?ƒ\ÉcNÝ¥ž_»\ï°*$‘\Õ[‘|\Ùû’\É\ä\ÇHJŸ…U_\Í\äHMÑ…{ŸO­Þ¹¯ªU¿\ôD¿c´œ…ûH¡²×„\ÖX\Èoú\Ù\õWú•’ÿ2}Ý¯\ö\ÚRlv4^_\çX\ÇuÏ\Í=\':]70\n„·£cY\Ê\Z‘\ìc››·7\Éx<’½T†1!ƒ|l_\"¿>\ãCy\r ’ 5\Éü\ê3’\Öq\í\ö6\Û6ž…\ä¥MF²p\'{eŠ#S¶žKMJx˜\Ð³‘¦Ô‰T¿ëŠžw\ÝzC\Ï	vL±9\÷ûZ¼ú\Ø9˜zW\ð\ó\'\Ûvœºn`DÐ™¹ œ™Ï¾…Hg$Ù˜€jª\ó¦E2±NCZZS\"¹Æ±‰\ë36\Ð50\â\r‘­H\ægP\"I™\ÈÇŸ<RH%s‘´\Ïy\Ý\Ú>#\éIHLÀœzŠ\ÙLj\ì\÷Î\÷±9Z®+:Gj½±\ç;¦\Øk\ÉøyÛ­iýZ%\æO¶\ì¸fN0\ì¤3j$vQO\ò±ÀF\"™7³f’Á\èzˆd¿c“\×gL\à\ò‘­H\ægP\"™*<\ÉKX$%&c\çÈ¤}\×vHB[\Â\Ã\É(6”\Z%]\Ñ1_>¯‰\Ì\á\Ðv]©­\í\Øzc\Ï	¿­\éÖ¶#}Þ¥p{ÿ\0P¯a“µü¸~N0\Ä%\Ï’7*SG™¨B®X½\ó\\g\õ¬>6o,fr5\Ö\Î‚\âED’¥¹\Zmm7“\ÛÍ{] ’ 5\Éü\äÉ}¤’,¶½Yd\Ô|	‘ø}•\Íh±\ÑcI\Ë1\Å\Í.ªŸÏŒs,Vœ\ÃÅ+\és]V¢l\Æ_?Ž=\'¼c¶^w³S:Ë¹†\×w\ä¹5]›\Ü\àZƒá„²I\öf“\ÊM\'Aybr§¥t™qŽ\ç)131‹†rlr\Þ@\ÌxŠYÖ¥]\Ó?Ÿ\È\Ø\Æ\"ª/ø\õ£‘­H\æ\'·Hú†¤1T’\"	‡5l\0†\çˆ$h\rD2?I 2§\Îg&\0`\ãH‚\ì@$\ó3h‘œÛ¹C	b“B}ÁzÀ¶\ÓUA6\00ü@$Ak ’ù´H\0\0\09€H‚\Ö@$\ó‘\0\00\n@$Ak ’ùH\0\0 ’ 5\Éü@$\0\0ŒI\Ð\Zˆd~ ’\0\0\0Fˆ$h\rD2?ƒ\É&wm/\í»\Å\ô\0\0\0\Â@$Ak ’ù´H’(†¾3\Ò\È$\0\0€&@$Ak ’ù‘Ü»wd\0\0@ˆ$h\rD2?-’;w\\®ú\Ø\0\0\0„€H‚\Ö@$\ó“[$O|\ç^q\ÔI\×G\ËkN\ÛJ*a‘œú\õ•Nø·W\ÍLŠ‰‰I1\Ó\÷\ïûQÜµŒk\ÂZc§\Æ\åX\ï \Ï€0½î”˜š\Òe\Úü\Þ\Ý\Ê\ÂtQW–®\è©VF¯[´Û±–2®û3z–Ð¼ŠH\ÌXw­5ZT\Üp»Š1½ ËŒ\Æo<\ï8°² ¦\åu€H‚\Ö@$\ó“[$C\òè—DR‰‹ä¤˜œ	µ\ÑOüå–¶¶¬5vj\\Ž\õ\òœ `¡0 ^å·“-$M¾(\êþV Ü±$}\ÕþŒè¼‘˜‰u\Ò\\Ý¢-ÄŠX˜–²\×\í²\ØŠ\'\Û#\"‹_?\ïA\")/D´\"™ŸAˆ\ä\Å\×> v\Þ\ô°x\ÓÙ·ª:z¤cª·\"y\Â\öU§Ô‰d§#e\Ò7 ùŽ˜\èt mmYk\ìÔ¸\ë\ä9P	WH$¹\Ü1(\Ã\ÇLª”M\Ù?\"eaØ¼Ñ˜w½nh\Í!\Â\çAst¤EE2¿ù¼c€|\Ý\èu‚H‚\ÖDE\òÀ\âø‰\ãÅ…w\rZ$é˜2`¶\ë›rsa„H¾\å\Â\Û\Å\÷?!\Þs\éAUwþ\Ëb\÷\ÇTýZ3’3‡\è±#,‡ÄŒ\ÊRz\çzhFL²\×\È\Ùgm“33‰qv›$V×™¹f¤ÀqB\Ù\ô›\ç\ó±~\Ñ5\ÆÏ¥²\Þº\ÕXó²®üX@\êZ\Ùs\Ç+ñ¯‰¤qo~\ç\Ø<g×Œ\Æ\è.\è\ãø5´s‚\á&.Œ¡\ìbE\ò¬ªG\Êþ™m\ßZ©,\ç\Æt\à\ë4\ÙF3Wh%\ó3™4\õh\×IskŽ\Å\ïg\ÞÍ\Í\ÎB$Ak&¶n\Û\àŒ¤ûF¨\Þ\ä&g\ä[\æ°\á¿a\Ç„Hs\ê.\õü\Ú}‡U!‰$¨ÞŠ\ä\Ë\Î\Ø\ï”z‘”Ï¤bC\"¡®½/#^ŸH›û\ÙJ\ïz\ÍwŒ´\è1¥À\è\ãB\Ì(#\Z”\Ó\Ïþm$\ÖQmk²^†\Ê\ÊVWP\â\Ç=§CsÎ\âù×¤i¯oe=\ìš\Ñx>:¶\×:2\'j\Â\Û\Ñn\ö“\É>¶¹y{‘Œ\Ç#QLe	}‘d\çIN,~Ý¼›\ò:B$Ak¶Ll\Ý!\É\ê\ñ°\Ð|]ƒúŒäƒ‡u\\»½MÇ¶g!y©I%]F4J©\ô\Ú=±+ú±±\Zœ\Ín™¢ù×±\î\ØR­w\Ö[#—Z/Ç¬½\"RF\Ät±\ã¼øE»)´ˆX¼o}\Å\ñÏ§\Úv›):»”3›±\ÎH²1\ÔT\çM‹db†´´º\"\é\Ì\ÅE2A,~,ojØµƒH‚Öœ¾eBœ\Ô%‘\Ü.\Þ<q¬x\ë[_-\ßD\Þ&®z\ê*qŠ\ÚÚ¾K\\4Yfq\ô†\êd†\ì›\ÏZ¶\Ãj\Þ\ì‚\ñuŸr+0²u\è½9–\ç`\æˆl§’„\Øú\ò\Í\Ô_gœA‰$e\"\òH!•t\ÌE\Ò>\çuµ\"©®|NÛŸ…d±vu\r\×*’¡¿ÿ:\Ö[üzýšëˆ­‘K­7€\Ý®\Îa®™\Z\ç\Åž³Æ‰\çà­£¯8þ9\ð\ãTÁŽk\æ\Ã\Ë\Ê ÙŠx¤\'yL\Ì\Z‰dd\ÞXÌšuZH\è¢\ëuD’ž—[\ÓE©‘\ÉXü\ô¼›.\äI\Ð\ZW$\'Ä«Ï½\Íd$­H>#~\ðy)\\\ì\Ý/ø&­×²\æ\ÆPo’!¡Q‡‘\íQ\ÛÊ»³\îST«7JK·cT¦)\ô&\Ê\ç\÷Ö’`P\"™*<\ÉK½HÒ¡\ê\òµ\ó\ÏÛ¿Ž\öZ¹m\îV±n«þ=xs\×[¼x‰uT\Û\Â\ç\â®7\õQs\Ò5rþ\ñ\Äcº\ñ«\ç\\R\Äs\à1ˆ~\â0¡&\ÔkZ‘:®Ÿ	AÉ³„\äm\ãR&\Ê3Û—?\×YD=«\Í‹™\\§Aµ\ó† x|k›Á3’4WH(c\ñk\ç\ÝÌ¸\×\"	Zsú–-\â\ÌÊŒä¹·Ù­m&’?ø¼|“ao\Ì\Î*\Ë\ÞQ)\Þ\ÑNŸ˜¬±\ñ¼O4¾\÷†hú9o‚ªÎ/*Àþ±+]ø-\'·H\æ{$ù¹Œ\ðk¾¾\î\õ0°k•¾\ÙF–\ÐkW{l\Ñ\õ:­\ã9j\Ñ5z\ñR\ëµ8¯¿½.Z\ØT¼VPF’s0\'p\Îý\Ä\á\õ\Î\÷~Üš\ã\à\ë†\r\Ê&ùY¹r‹6$^L\îÔ¡”.3\Î\ñ<%W&f\ÑPŽM\Îˆ\ïO1Ëº´k†\Î\Ç\ÉXü~\æÝ¼øY]ˆ$hMùÉ”Hþ@¾\Ç\èˆ“QQo<¡7\Æ~¼‰Z¢\ñ\Ãchm\ô¨\Þÿc‰¤3.²…YCn‘\ô!9Ic¨„E\0\0À8\âü£B‘­Ùº\Í~ýOZ$•`©L—3’«¶\Ûa)A‹Å)EW-’*Ž ú\ã\Ù1ewj·0\Ó@$\0\0#I\ò{$kD\Òn\íù\Û]J¶\Úl‡\ÕZ0¾7&¶\å\çŒ\ås$D²\éf‚A‹\ä\Ü\ÎJ›\ê\0\0\0„€H‚\Ö\à—m\ò3h‘\0\0\0r\0‘­H\æ\"	\0\0`€H‚\Ö@$\ó‘\0\00\n@$Ak ’ùH\0\0 ’\ãÀê’˜›³¬\Ì-­š\Æ\ö@$\ó‘\0\00\n@$7;Ë‹J—\Í\ñ\0€H\æg\Ð\"\Ù\ä®\í¥}·˜\Þ\0\0\0@ˆ\ä¦fU,Í¥$’\ÚÅ²‘M]\ä±im\nD2?ƒI\Å\ÐwF\Ú™Bè«¨ø\÷“?\n\0\0Dr3£¶´Sb¨Es–™\æ\êÒœ˜[’-ÍH\ægDr\ï\Þ=\É!\Ãþ\ò•¾¿n\0\0\0Dr3\ÓH$\ç„ûq\Ée±8\ë×¥H\æg£Er\çŽ\ËU[\0\0\0€\É\ÍÌšD²n;¼\nD2?¹E\ò\Äw\îGt}´¼\æ´=A¡¤Iú\Íq›\ãerf¾üUU\Ü\ß*/¡_ù\áýd	¤\Ø\Ô<•z\ö\ËAª„\ç\å¤\â\Ä~…(\\ž«IŒD¼¾úŒ8ê—¥b+`\ôºSbjJ—i\ó{w+\ÓE]Yº¢§Z½n\Ñn\ÇZÊ¸\î\Ï\èYB\ó*\"1cýÝµ\ÖhQqyûŠX˜.cvƒ}\ç>v¬,ˆiy ’›š:)µ##9\äÉ<ú%$‘T\ÒIOrÍˆ3%;Á\Ï\ò\Å$‹¡>\Èb\Ò\ÐdŽ\ØXN2Nl}ú\è\\MbD\â)±\í§Ï¨b6U^?ˆ\äú!`¡£^å·“-$kUY¢þV\ÌÜ±$}I¹Š\Î‰™X\'\Í–@‹‘Án—\Å&z¢g”…$4\Ö\Ç_s¹ž±„®| ’›\ä]\ÛZ$\ñ\É\ác\"y\ñµˆ7=,\Þt\ö­ªŽ\é˜\ê­Hž°}\Õ)}‹¤eš\Ö(’\ôyÀI\ÙÁ>F	\Ì\Ñx,Ç‰[_µ>>W“~-Vù~ûŒ:t.É„+$D\\\î”‘cWÊ¦\ì?½ £5…\Í\Éq\×\Ù\ë6•¸\Èy(RmÖ‡Ä‰c½\Ìnr\ä\ëF¯Drp\î\Ê\ÖE»£\Ù\Ú^\Â]\Û\Ã\Æ D\ò-\Þ.\î¸ÿ	\ñžKªº\ó¯X»<¦\ê³e$=(\Ë¹:	\"Y2\í*\ã’QMuŽ\æc9nœ\Øúüú\Ô\\Mbx}Hf\Õy¿}BP;e-M\ák+2šT¬À™x\óe[\õº\Ú1\öfw\r$\Ó<Kª²¼¦:{Jq ’C\\C\ÙÅŠ\äY	T”ý3[ÂµRY\Î\éÀ\×\én=‡\ÖY’E>=­\ÙY—\ÙD\Ü1ÁŠ4Dr¬1\"\ÙOú1\0D2?ƒ\ÉcNÝ¥ž_»\ï°*$‘\Õ[‘|\Ùû²&‘d’–HÂ“¿¯#eL\Ö,©9\ê\Ær¢qª\ë+‹—œ«I~ý\Ú<\á\÷\õ„ÑŽ“bªÏ\ê\å\Ú\ìù¨kcûi‰¬¾ž\Þ\òü‹1j|d\Î\n\Ô‘\Ü\Â\ÛÑ±,eHz[\Ï)Á\ã\íMD2„.•¬\nÍ§$”\Ï\á‰d°¡¶ºµÀúM\ãEù7‘k ’\ÃÊ >#ù\àa\×noÓ±m\ãYH^\Úd$u†*$þ8\÷\Ø\ß&Vq\"7\Îøs\ô3–\ãÆ‰W?\ël£|Ïˆ6\é‚\ÚKy-–\Å\ä¹(ª±\Z\æSMŽrÜµ9\Û\í\É!Gg\õ‚rf>û\")’¾˜cT\çM‹db†´´\Öd$\ë>\ç\Èû`k»„]ˆ\äX‘V%’”‰|ü\É#…T\Ò1Iûœ×µúŒd´Ý¯\×/-;\Ôæ‰Ž*1\Ñ\à±ú\Ë\ñ\ãÔ­»n®¦1\äs\ÚN\æ[\Ï}\÷	Á\ÛY¶´j\ØkR7†\ÖQ-\ç\öº\ð\Ø>4®\Ék\ò\Ï8$vQA\ò±@_ýcEd\ÞXÌšuZ\ÒB—Þ‚n\"ƒ¶OZx\Ç~- ’ 5\ÉüJ$S…g!y\éG$\Ít\\Y \Ï\ó5‘%*\æØ¹\é\ÅRJMrŽš±œ\ôZ½\õ°úÚ¹\Z\ÄPÏµh¹\ë\ë·O\Þ\î¯+¶M\Í\êy\Ô\ãcc\Â[\õ|¯A\í\Éu#)@!yc\Û\Çjk×Š\ßV\æ\ÏuQOÁ\êc\ó\Æb655\Ö\Î‚\â1‘\ì\õ\Ê\çþ\\6\ÛØ¤:LgJ7/\î5…H‚\Ö@$\ó“[$sd‰\'J\ÆlŠJL¬€”\ÅJ’»}[Rl\'\æ¨\ËI®5&>e}ý\\\õ1\ôs9·¿¶¾û„0\ãl\á\ã•$úm:^§Sf\Ý)\ÝxºM×•×¡\\]ŸR´\Ëú0\Ô‘\\/(›doT±¥\"O¼L¦Ô¡*3\Î\ñ<%u&f\ÑPŽM\Îˆ\ïO1Ëº´kz\ç\Ã\×\È\ÇrIŒ\õ‘8kJO¼i\á×ž\nD´\"™Ÿ\Ü\"\éCr’\ÆPI‹$\Ø<\Ô\É\0\0Hº`ˆ$h\rD2?I\Ð´™B]Ö’ÝƒH\0\êH‚\ì@$\ó3h‘œÛ¹C	b“B}Á8\0‘\0\ôD´\"™ŸA‹$\0\0\0ˆ$h\rD2?I\0\0\0£\0D´\"™ˆ$\0\0€Q\0\"	Z‘\ÌD\0\0À(\0‘­H\æ\"	\0\0`€H‚\Öl\Ø\"Î¼Dr»x3}\õ\È[¯\Ð\"y\àq<ûJ’\òË\Í×•x¿\n¢N\Í\Þ5\ZúJ\Þº»Ô«\÷¾tYi²þµ\r7®ùª§¿ýú“~Î´…¾„:7ƒ\É\Ë/¿\\lß¾]\\v\Ùe\â\ÒK/\Ý\î§\Å%—\\\">ù©O‰O|\â\â\âm\Ûdýe\âð£š\0\0\0@ˆ$h\É\ÄY\ÇLˆ7\ï´\É+\Å)RºN¹\Úd$^$E\ÌÁIûÛ¿\n)xY\ç\õ)\Ûù±\ßf\ñûT\å\Õ=ŽÅ§ÃŽF=®^þS~dP\"Iù\ì³\Ï\å*Ï”…D\óž{\î\ÝOZ>|ØŒ\0\0\0\Â@$²º4\'f\ç–Äª9Ö¬Š¥¹Y1·\ÄjW—\Ä\Üì¬˜-Êœ\à\Í•~²ø\ñ›\Æ2\ëà±œ5\rÉ£žÇœµ»\Ü\Ú\Þž8~\âq5\ÛÚ¦ŸL+VM\Ê\ØL§ü\Ù6%n3L\æR¢g\ä®(<{ª×¸?i\ç\Å\÷2ŽŠZ›¿§\ÒÁ0(‘¤L$	\ä\Ó\òuyú\é#â©§ŸO=\õ´ø>•\ï?¥D\ò›\ßü¦’\ÉO]r‰\0\0\0„H\öÁ\ò¢+hJ.—Í‘dy±*{Fy7\õ\õ\Çr‘\ì\'–É²/­k}ErBŠ\ä\Ñb\â\ä\íý‰\ä!\ÚfÖ²7ß¡c.m¾À\Å\ÛJAd\õJûI·¿\Æ_‡\Þ\ZU‘¤\ílÉ«¯¾ºRH&I$\Ï?ÿ|Uþ\áC6£\0\0\0€0$G³³‹B»I5³¥Š“)[‹E\Z+\ã(²\í6.abW-H	\ZŸC	Zƒ‹S“9Øš*\â^»¾^©d	=^\Å\ó\ÅO\Í’<I¥¯>GG\öœ>ý\Å\Ò\ë*¯\Ãú‹¤þŒ\ä\ö“\'Ä±\ç\ìKlm\óÌ¡–3ú\\¤\ÊDV²¾À\ÅÛ‚\"Y¾T<‚ŽCŸ\ô\ê£Â™—A‰$}&Re$m6’mFR–\ï}ÿ)UŽ\È\×l\æ>dF%˜\ïT2¿Q\Z\õ\õ_\r½\Æ\ågd\0m\éu§\ÄÔ”.\Ó\æ\÷\îV¦‹º²tEOµ2zÝ¢ÝŽµ”qÝŸÑ³„\æUDb\Æú»k\r¬Ñ¢\âº\í\Ñ50R\ñ\ë\Îq\ó\Ó]:ÿ®¾*³‹‹LB<#H\Æb‚£D•\Æ\ìG	¡76–e«Ê‘AIc?s\Øø$W|®\Ô\Ú5Ì®7xn¼-tZž(rA\ì3–/—%’<²[œs¬|\Ã\õ¹b\åf›˜\ÄiQs3•þs¢:¦Ü†®\nª\ÂÛ®v³ˆ~|‰¿½\Í\ä¶Ó¡BqCn‘ü\ÒÄ‰\Ûe\é\Ér›,_5\åVY–d\Ùg\Ê-²\Ü,\Ë^S\öÈ²0\ñ£&\n\ÇÜ´\Ô\é\È\ëS\'‡ý\ôM½.^=\0`m¬,ˆ…ÂŒH\n\ÂBD2U-\êo\Å\ÊK‚3Et\ÞH\Ì\Ä:i.\ã1V\Ä\Â4\ÉN—Å–4<\÷Xü\Ús\ôu›ž\Ö\×nbi•g³¸ˆHj¸\à8\Â\Ç\å,0Ö‘Ó¾´\èHŽª%?.§f}¡9\Ô9y¢–\\»¦™€\éq\ñ\íKþªs·Iº†|\Ý\ë-’›û\ëb³\äI’\ÈoOü¸xL–UY¾%Ë£²žøoâ›²|C–Y‘\åaY’\å\ë²<(\Ën96]Ÿ†\ÉF}ý\ëm3\Ë\ó:\0°ù!\á\n\É—;eø˜a•²)ûO/\ÈhMa\óFcr\Üu\öºa¬9E\ì\Üc\ñû=\ÇÍŠÉ®¼F\ô:Mh1i(’*;H\Ù8·\ÄE’“m\ç\ó™\çž\ä©,£3Gb}•9\ô˜ŠH%×®i\"`jmr/o\ê:5–¿ª®]$«± ’9\Ù\"I™H’H\Ë\Ó7\ìþ\èÌ‘?ø\ö\ã\â;ÿû\ÝJ\"-ß¿\á\ËâI\Úg™a]\ï¿&þ±É€d\÷XZ‡Wùj\'+¯:š‚Ö¡\î\Ü\÷\×!\ÇU\ÖGøý\Ê6\÷k®(4_\ác\æs\n\ëŸ\ÌÀûø\ë“c\ì€h\Óo\Í_\ÛEø¯Elý\ö\ï$´Î™\È\ë){\ðkY,œ\Ç ü˜e[\õ\\bm!\Ìúlq¾é¡¬\×ËŠýMnqae\Þ*’g%P=R\ö\Ïlû\Ö\nW9o4¦_§\É6š¹B\ë,‰œŸ‚µÑœÅš#\ñû>\Ç\Í\n]7m}ýúIOø\\¸\ÐY¸ä”±­\è\Â\Ã\ã*\á\ãå¯¯\Éº_E\ô¢k\×\Ô\n˜#x¾À…\Öf\à’H„\Ö\â\ô\é#{!’9\ñß„Ö‡\Ü\"I\ÛÙ”‰$¾ý\Ê\ß\Ï\Þ\÷€xüOVÇ”‰|TÖ©\ç\Ï¥z¤L$I\äý²\ì\Ú0‘l\òœ\à\Çú\rºúYW\"4N¾‡¾Ú©X\r	Š>´1|\ÙL­\É{>É¾\æJ\Í’¦us°\õ\ðs	bÇ†\Î#GYû\×v4_¨¯\×O^\÷s\Ïþ:	?6\';\Ú&Ÿ\ó\×&\Ù‚\÷·P]\êu	Y_\Â[µ\ñL]R$½­\ç”\à\ñ\ö&\"g¥\ÆVˆ‹¤\ÓI‹\ß\ç9n^\ÊkB× ?‘L	Žik\ôùEsQ,:Ç¦Ÿ\'J*†\'’\Í>#\é¯\Õ?®’°Àø\Ôy\ÙAunÌ§/k‹\ÅÏ·\Ä9>&\ö¼%øe›ü\äIú<$mg\ß\ï~F=~\Ód$\ív\ö³\ß~\\þ\Í?Pu”ü\Î\Ì\Ç\Å}²þ\ËÁ\ÏHZ\èp0\"Y\ÞD\å\Ö\ë\ç~6Ç´9b\æ\Ãcþ±žS¿\éS¼\"§\ÇLVd5»|®ã³¶\\\"8\ï\ò\\Bè±•\óH\Æ1\ó­ùk»:œ¯š\×{M\ÕºO\õz~l	ý ˆ\ÑdM\å\ó\Êk“lh¯}]\êbuŠ\ÐÊ‚˜®d5\éŒ$AMuÞ´H&\ÖiH]H$\ëcrŠø\Ïq³\Ã\äZþ­\ô)’\õ\ç\Û\Ã\Þ\Ø% ¿pc«;¥­\Å8sha³1æ––\å\ñ\Ú\æ(\ÖZ\ØRlíš¸Hš5¬K¿>F\Ð\Ê9\ë\ñ‘\ðE’H\Ær¯S°\Ðz¹0Æž·\"™ŸAˆ$}&’xL\Ê\"I$e\"	’\Èoý\á\É\â™ûP™H‚2‘$‘ÿ!\Ç}i#D’¶›-Tþ†\ë¿ù²\ãÀwIbœ\Â\Íz\éo8T<jhŒ”š\ÉI\'c™Žmž\Ó919²}\õ–©/?!s¬I$\ç\ÑD$\×üµ]th?\" Ê¶\è\ëF}B×›\ðb;1b™O‚›\çÁ\×&\Õ\"\Ð^ûº\Ô\Å\ñŒ#Ab\õ#Ož\n	l$Y‘yc1k\Öi!Ñ‹®·\"’\ÍbrŠø\Îq`\")¯g\Æ\ï‘\ô%n¬\Ç£BÍµ 1\Ía‰\r€H\æ\'·H\Ò\Ý\Ùtc\rÁo¬!H Ÿ¾m¿xT\Ê$mgV\"—7D$µT¹\ÞÀ\ßpý7_~¬e°š½\"B\ãX_ÿMŸŽ¥0Ñ–fh.W0ck\Ò\ó„3d|½~Ÿú9Šk3K9¶z±8\å-\×ý~m—<Š^3z\Î\Û,ew,\á\Í\Å%U­›\Çfý\ó†_›T[ˆP»Ž]ü1ü8\ö<I\n‰–›š.ÄŒ…+”\ñ\ÓS°úØ¼±˜MDMµ\ó† xL$c1©>´µ\íÄ\ã¸Á¯C\Ö/$‡H®/\É\ÍLn‘¤¯ø©»;\Û~&’Kä½²Ü´\"\éZ¤$\õ¦\Z:\Ö2\ê\nix\\ê«H^\â™G-Z^\Ü9\ËB\ç«\ÛB¥\â‡2tAüv\ïXIŠ7‡\àcùy\Ða,C\Ï\í\õ\ò\ëCc¼9^_g^YTp\ÞÇ\á\Ïe\Úi¬\ó\0\êgê’~m\ì¸p[ˆH{\òu\ñ\Çøó‡ž·‡2~\öF’\Ê\r%¾x)\\qP\Òe\Æ9\"¥¤\Ë\Ä,\ZÊ±\Éy1\ãý)fY—–9\÷|¢1‘L\Äž\ã¸\áþ=@$Ak ’ù\É-’_2ûžÈ¯\ÈBwfS¡k\è3‘”…¤By,›“ú7g=_.›C\ñ›J6X_\ð\Ú\0‹Œ\"	\Æˆd~r‹¤…~\öPý\Îvƒ\òÞ³\ßgF5…ÞœyÆ‡J\ìÍºŸ¾ƒ¢F$)“\äd\Ðúe­²’\ó\Ú\ÃuF\Öú\Ú¸¦\0p ’ 5\ÉüJ$\ég/š™\\x‘8ÿ‚\Å\Ï?_œûÁ\ó\Ä\ô¹\çL@¼\ïœiq\öûß¯$\ò\ï\Ï:ÛŒÚ¬„D\Òn‘\æ\ÛJ\0€\Í\nD´\"™ŸA‰$\0\0\0ˆ$h\rD2?I\0\0\0£\0D´\"™ˆ$\0\0€Q\0\"	Z‘\ÌD\0\0À(\0‘­H\æ\"	\0\0`€H‚\Ö\ô\'’±;e\×J\îx\ÃAn‘üú›Ï­”OŸøV\ñÄ¿¼[ü§)\ôœ\êB}\0\0€I\Ð\Zˆd~r‹d\ïW¶\Êÿ«mù\Ð\ó]<úŽ\ç;…\êx[\0\0\0€I\Ð\Zˆd~r‹\ä\ÒKÿP|o\áE\êÑ–‹~\ö8qøÿ<\Ï)T\Çû\Ø\0\0\0„€H‚Öœ~\É\Ýg‰cß¼SŠ\ä\âmÇ‰.8¥ø\å‡É‹šÞžøy¿¯\ËŽNý±m\ã\rl\Ì\ä\Ì‹\Ç~kW–µÿ´\ÝÆ“[$¿\ò\â\ßU\"I¶œ\÷\ÜW‰oü\ï\ç9…\êx[\0\0\0€IÐš-§_§Dr\÷YÇˆc\Ï\ÙgDR\Ê\Ü)W\éŒ\ä5.\Å\Îþ„IzÎ„O	b(»shfR\Æ6m\óW8G˜\Ü\"ùw?ùR§œ\ö¿(\Þ\ð#\Ïý\ÅÏˆGþ\ê\çT¡\çTGm~ÿ(tÍ½Ÿ‡\ãÿ\0˜,^\Ì\Í#ù\0lz\Ý)15¥\Ë\ôÂŠª[Y˜.\ê\Ê\Ò=\Õ\Ê\èu‹v;\ÖRÆ^“\"4¯\"3\Ö\ß]k`\×m®\Ñ\ï:\ÇºNIÐš-[N7\Üwƒ8\ë˜c\Ä9ûhk\Ûd$Ø­\ík<4Ï•8V%¤%)V>\Ø\ç\÷ýx\\^F—\Ü\"ù§\öE§ü\î\ë¯»?w“¸\ëQ\â\á¿üYU\èùW®Þ­\ÚüþUŒv:\òú³\×P¾3Åû€y[x\Ý\0\ë\ÈÊ‚X(Ìª\'º\é#Y«\Ê\õ·b\æŽ%©H\ÊUt\ÞH\Ì\Ä:i®n\ÑbE,LK\á\ëvYlI“s\ïwãŠ¼N\Ó\Ó]ˆ$h\Ï\é[¶Š\î\rgŠcŽ9K\ìSŸ‘\Ì ’NIK‘4\è,\åhg½r‹\äÿ\éu\ò¿ÇªG*¿q\âN\ñƒˆ{\ßø\ê3®T\è9\ÕQ›\ígKºþ1)d¯›Cj\0`}!\á\n	—&e\ä˜Á•²)ûO/\ÈhMa\óFcr\Üu\öºM%.rŠØ¹sú]\çø`\Ï\"	Zs\Ý\é[\ÄI\'$Ž9k·¹Ù¦¡Hª\çLø¸<R6\Ò\n£ªq¶¶T?Ê™\É\Ü\"ù†7]­>#IT&½+VZ·¿ø‡M¡ž?¶\ò¸j³ýl‰“’\ÂH\Û&ú\0£O\\C’T‘\'+Wê‘²fK¸V*\Ëy£1ø:I\î\Ì<µ[\Ì)‘dm4gp\Íý®s\\(\"	Zs\÷u§‹£\'Žg\í¶wm7I‰’DoûZÁ>S7\Ùž\Ùb[\Þ\Î\Í6\ÎVøhg¼r‹\ä\ï¼nN‰$=R9æ¸‰\å{\ï7þ—ÿbzq\ãýª£6\ÛÏ–8q‘¤\ì2—y›)†D0<„·£ã™º¤Hz[\Ï)Á\ã\íM-D/•UŒ‹¤3\"’ý®slP\Û\ÚúzA$AkúûúÐ„\Ü\"ùÒ—ÿ¥S^\ô*>û™«Ä7\ßizq\Ç\Þ\ÛÅ•;¯Qm~ÿ8!‘\Ôÿˆf„•\ð\ó4\0\0\Ö\Õ\ÊIBD’\"\É\ÇD%«:oZ\Ð\ë4¤¥5$’\õ1û_\çxÁ¯D´\"™Ÿ\Ü\"ù¼\í¿å”Ÿ\íž ~\ä·Fœ\öŠÿ*þ\æWt¡\çTGm~ÿ8¾H\Æ>\é\â\ÜT\0XgH’\âY<’„¨y\òTE#‘Œ\Ì‹Y³N‰dt½‘l³\ßuŽtMË@$Ak ’ù\É-’?w\É	\ò¿ÇªG[~\â\Ô_\÷ü\ÙsœBu¼-q<‘Œ}þq~žÉ¦\÷\ñ\0Àú”<KH¢\Ø\ö1e+1c\õ\ÎsŠa\åŽ\Õ\Ç\æ\ÅL®Ó \Æ\ÚyCP<&’±˜To·¶û]\ç¸Á¯•\"	Z‘\ÌOn‘|\îG~M}F’mù\ñ·¿T<ù(§P\ïcKW$‹\ÏA²¢¶¸\Ï\Â\"	ÀFB™4›M²¥Ì¬y\â¥\ð¤‰DÂŒs|K‰–‰Y4”c“\ób\ÆûSÌ².\ä|%\îùDc29\êw\ã†ÿQˆ$h\rD2?¹E\ò9\ç«D’mù±·¼X\Üu\ÒO‰»M¡\çT\Çû\Ø\0\0\0„€H‚\Ö@$\ó“[$ÿ¯?z~¥ü\ð¯þ”¸\ê5?*>o\n=§ºP_\0\0\0 D´\"™Ÿ\Ü\"ù\ÐCµ*\0\0\0@ˆ$h\rD2?¹E\0\0\0I\Ð\Zˆd~ ’\0\0\0Fˆ$h\rD2?I\0\0\0£\0Dr,XKs³bv–—9±´jš[‘\ÌD\0\0À(\0‘´H..›CbyQ\Ê\ä¢\àUk\"™ˆ$\0\0€Q\0\"9DR*\ä¢\É\åE?[)\ËÜ’\Õˆd~)’\ôZ<þ\ÄŠ{\î{@\ì\ë7\ßv§¸¹w§\Ø\÷½²\îA\ñøwþ¯\0\0€F@$Ç‚ªH®.\ÍUd‘\ê\æÖ°\ß\r‘\ÌÏ D\òÈ‘g\Ä¯ˆ\Þ\×‰¥;\îR¹\ï\ö¯‰}û¿&¾z\çAq‹<¾ý®{\Ä\×ù†xZ¾v\0\0\0@\nˆ\äXøŒ¤›žT@$‡‡Aˆ$I\ä½\÷?¤riÿ]J\÷\Þv‡\Øs\ë~q\Ë\í”H\î£\ÇÅ­w\Ü-\î¹ÿ\ëj\0\0\0\"9\Ä>#\é\Þp‘r‹$]ÿþ†\Ê>\îù\ê~ñ•¥ž\Ø-Ë—oþªX¼\é+\âŸvþ‹¸\äŸ>#>u\Ùå¢»}‡ø\ì\çÿM\ìý\ê\âþ‡V\ð\Ú\0\0ˆ‘BŸ‘owC$‡ƒ\Ü\"ù\í\ï<¡2_Yº]Š\ãnq\Íu_\óÿ~ƒ¸\öúÅ¥Ÿ™¿úk¿&^þ\ò—‹_y\Å+\Ä+_ùJ\ñÛ¿\ó;b\ç¿^¥2—4\Ög¾3!:\ó\æ@1/:“b\æ9$\æ;b\Â\í\ÔŠ71aJG\Î\0X+½î”˜š\Òeza\Å\Ô\n±²0]\ÔOMuE\Ï\Ô;\ôºÁ±DwZxMŠØ¼±˜­\ÖI¨¸^{bý>jž\éQ\ô\êc\ì\æ¥\'º\æ\ZPHŽ‘\\]s\ÈH-¹E\ò\à\ò}\âË·|U\\u\í¿‹ÿq\Ò\É\â\×\ã7\Åoœ\ð\Z\ñ\Ç²U¼\óŒ3\Å/þ\â/ŠŸÿùŸ/~\ñ‹\Å/ý\Ò/‰WH¡ü\èÅŸR\âypù~…\áK\â¡1)o’™ä¡™I\ç¸*>“Gy<“4É€\Ø\04+b¡0+’‚RúHÜºQ+#¨¿³\êØ¤\\E\ç\Älµ\Î±0-E§\Ûe±‰\È\\A¨]\Æ(D²Ÿ±›\÷\Ü!’cA\à3’²ø“l%’7œ)Ž)²EoWZ‘¼\ëBq|Q\ïg±@Œ\Ü\"I7\Ñ|i\ï­\âC?\÷s\ÏGu”x\Îsž#~\ëw^+\Þú?ÿ\\¼\ð…/¿\ð¿ „\ò%/y‰x\å+·ˆœý„\ZCc+\ØM\Î\ëi$YW¼À‡\Ä\ÌdF‘#qe\ó\Õ‘ $\\\\\Ðj\äˆ2r\Ì\à(c§\åQ\Ê\Ï\Ü\Õ\Â\æ\Æ\ä\ô¹\Î.’Fsi¨­»° ¦\íy\õ1vs‘™¹û\îmâ¤‰£\ÅY»MFòŠ·Š\ã\Î\Û/E\ò*qŠ”\Ç?¿\Æd$UV	o\îM\È-’_ºùVq\Ó\Þ%qÑ‡?&ž\÷¼\ç‹\ç>\÷¹\âg~\æg\Ä)\ñv\ñ‡oú#\ñ‚¼ \ÈF¾\ô¥/[¶lþ\Ø65†2™U¸(\Ú\ç$o6kÈŸ“–ÿ˜(3™Z\ö:IYO}ü\Í\ë\ì&\õ-3š\Ô\æf<L6TÇ·q\ì±,j>»ÎS\ó°\Ù\á¢e²xf\Ë2$Iy²r¥)ûg\Æ\×Je9o4¦C\ë,qE2¹~¾\æ)TO¦¾\Ù:\Çˆ$\È\Ì\Ý×.Ž\æo\ÜT\Þv¥x\êÀ\âø‰S\Ä5lk»ú\Ù:\"·H~q\×Íª\\\ô\Ï¾\É½\èEâŒ¿{¯øµ_ÿu\õ\\‹\äKŒH¾J|ø\ãR$\÷,©¢|-¥ˆ™lá¼”B\å`\Ñ\ÏGúW•\Å\"\óXù‡	«þû*C\óxt\Ø1\ñ¼ú\äqÝ¼\0l^\â\ÛÑ®,X’\"\Æú\×ms\ó\ö&‚\Ö\ï:K\Ö\"’,û	‘\0‘™\Ñ\"y’\Ø\îF\"¹fr‹\ä—\÷\Þ*®ÿ\ÒqÁ?|D<ÿ/P\"ùª£\ïùû³\ÔV6‰$\ßÚ¦Œ\äG.þ¤¸\ñ+ûÄž¥\ÈÿQZYd\Òh?Yù|$\õ!YS…\\J\öhX\à\ï\Åd U½“4E5\Ô\Å\æ\Ç\r\ç`S¡³za9Ó„\ä-)b\\ª¢’U7-hk[gIC‘d8} ’ ’ 3zk{Bs\Ön\ïf›\Ð\Ö6»aD\É-’w\Þ}\ÎH~ø£jû¹?ý\Ó\â\÷^\÷û\â}\ÓT¿\÷û¿/^\÷ú?\ð†7Š7þ\á\ñ¿þ?\ñ¹kÿ]Š\ä-\âÀÁ{Mz=\'g\Ä<}>Ò¾¨T×™q?\é¼\î|K¼N\öt2$t$ªJ£Su±ùq\óy\Ø°Œ[´Š\'y\òTÈ•/UAÉŠ\Ì‹\Ùf®H\Æ\ç²PÿrÛ¼($“µc\Çˆ$\ÈÌ¶\Ê\Í6²\Ð\Öv\åfþf\rR\ä\ÉGW_ºyI\\ùùµ•Mwh¿\öwO¼\ó\ô\÷ˆ\÷\à<qýM»\Å\rR4¿|³¾¹†~\Ý\æk\÷> ‰o=\öm\Å\Çn5û‚FuL\î(\Ü6\É\Û\ê\æ’8/\å´\è§\ç-·°CŸi¬‘C•!\å\ëˆ\ÌÀf$(y”‰+d‰ƒª·bÆ…‚?\×YD=«\Í‹\Ù\÷:CP<&’©¹Š­m\õ·\õ\Ñs7\Üs‡H‚\Ö(‘\Ä\×ÿd%·H>û\ì³\â?xH\Üq\è?\ÄUÿ\ö\ïb[\÷2\Ñý§Ïˆ\ËvÌ‰\ÏüË•biÿ×”<¸\ç~\ñµ\åT?\Éo®~;ùÚ©Ì •Dm»Ÿ´\Â)\ËdGtj2’ú\æÝ¿£e\Ï\Ö;\ñ•øU\Û\Ô:x_¾½Þ‘\ëpD26/\0›Ê¤ù7Y#A(\ëJ‡ó¤‰¤«\ÒG¢DËŒ/\ZÊ±\ñy©[5fÿ\ëA}™H¡\õ7I\"v\îc…û\÷\0‘­H\æ\'·H\ÏH™|\è›\ßw\Þs_\ñ‰wIi¼ý\î{•D\î?¸,\öß½l~sû€X~\ð!qD¾v\ë‡/–\ë\ÅF\Í\0\0£D´_HžŸAˆ$\ñ\Ì3ÏŠ•GW\Å\×\î¹_\ÜÜ»S	ã‡\îS\Ùû\Ú=âŽƒÿ!e\ò^\ñÀC+\âiùÚ­/I\0\05 ’ 5\ÉüJ$	z-žx\ò»\êw´{ªm\í\Û\î<(\î^¾_<\ôGU\ÛÆ¼^I\0\05 ’ 5\ÉüR$\0\0€\\@$Ak ’ùH\0\0 ’ 5\Éü@$\0\0ŒI\Ð\Zˆd~ ’\0\0\0Fˆ$h\rD2?I\0\0\0£\0DrP¬.‰¹¹%±ª\Ä\ÒÜœX\Ò›ˆd~-’s;wˆw\öŽdY\Úw‹\é\r\0\0\0„H\å\ÅY1;k\Êâ²©\Ý|@$\ó3h‘$Q|úé§£2	\0\0 	I\Ð\Zˆd~†A$\÷\î\Ý™\0\0dBeËŠ-XÚ‘+³h²”‰4Úž\rg\ÖT\æ\ÅpY‹,\Þ\\p\×Ä¶ýX,\'«Wiwc\Ï\Î.\Ê\Z‚\â\Ù\ç\Z\Ç\Ö\Ñ8·½v+šÚ1\ñ5\×\Ï\Ïi;—\rü\öÁ‘\Ì\ÏF‹\ä\Î—«>¶\0\0\0\0!TF’$\'¸\óº¼(\Å\Ä\n•™\ô\Ä\äE	Ë£¥\ÚGÉ¬\êªq˜:\òE1™ˆ\Ñy,.2yl+’uk®›Ÿ\Óv.:w|\ô\õ\Éü\äÉ£Nº¾¶„„’Ê†‹\ä|GLLLˆ‰\ÉŸ ½î”˜š\Òeza\ÅÔ–¬,L‹©\éQm‘\ôºÑ±e\ÜiŸ73\Ö_­\Ï\ÔOMuE\Ï\ÔWPq\Ý\öºs\çT®C\â\ÜÇŽ•1-¯ƒI-*a\ñ\à\Âe„giÑ‘\Z%-K\\\ÂŽE\ö©\ÊQP$¹üU\ä\Ë[\÷*?—–\"Y»\æºù9m\ç\â\Ï	Š‘u!’!I´¥‘\\¯Ÿ¤y&Dg\Þ\â\çh€…Â¬z¢[‘>ª“²Ij³b\æŽ%AK\ÊUt\ÞH\Ì\Ä:i®n\ÑbE,L\Ës\èvYlI\í¹s¨_‡\È:\ÇIù\"¨­m.*\ÛÅ·I‰		‘y\îHƒ2q¡zN°OU†‚\"\É\Ç:\ÂE\ã\õ\órœ¿n7¾\ÚzvD’_[\Ìø\Ú5\×\Í\Ïi;—>>–Ÿ\×z\0‘\Ì\Ï 3’\ËG=nÿÂƒN=I\ã	\ÛW2\"\É\çH.Wˆ(\×]’I\Ê\È1ƒ£¾Z¥X\Å2˜AØ¼Ñ˜w½nS‰\ã\ò\çS=wN\å:4Z\ç!¯±µ­d‡¤Å‘.?$/:\óeå¨¤˜H\Æ\ê9µ7MH$ºH:\ó{\"§Î•É—“U-Ïµ€Ç¯]sƒù\Ú\ÎU½V\Å\ë¹N@$\ó3¨Œ$=žûÏ‡\ÔãŸ›8z\ê\ËE==†JH$)K¨¶›©t\æÅ¡™\É\ò\ØÔ…9$f&\Ë~E·C3b’\×\õ:i\ë&gf*\ó\0\Úâ‰–\É2©Ç€V\ä\ÉÊ•z¤\ìŸ\Þ\ön‹”\óFc:\ðušl£™+-s)‘dm4\'_s\à:4[\çø`³\ÂU‘d\âG¢V\ÍHª)H‹b\Ñ9	#©“šj5¯¯*’z\\‘}s„‹\Ú\äúhÛ½0°˜\Èœs`\çj©\ÄO­¹Ÿù\ÛÎ•IÇ¬!\ö<\ÉüR$\áÞ¨©¼»{WQO/;c¿Sb\"\ÏR}Gþ7}Þ±\"€Z]©´±ýyb\ó\0Ö‚»\Í2tkIo\ë9%x¼½‰ \Å\ã‘¦²“q‘tb:\"¾INy\ô]Ûž´\Ø,\Ý\ÜÒ²¢²­µlM„\Ä$(’‰\ê\å\Î[\ÝÊ¥)¸HšþÜ„\ò\å\ÞažS$‰Ôšû™¿\í\\\î\õ\ÕÅŒUq/’[Og=!N\Þ\ÎD\òÊ·‰‰\ã/w¹Zü9e&/rn”\Ð,&NFÊŠHL\"Ü¬V9&&£\'ƒI\ÊBZ‘¼z\Ï#ŽH†J?\"9ß‰e\Íkj\ê&ù@U\ç\Êg\'\ö7`\0kDg\õ¸9¢´¦Œ$“ª¨d\Õ\ÌK8c«ý}\Ò\Ò\Z\Ét\Ì\Øu€H2\ØuÁ\÷H‚Ö¨Œd\÷$1q\ò\öB$¯|Û„8\å*\ÊH’H/&\'ù›¿Á\Îd<\ë4\ß1¢Q\'M%#V?¼R$?v\Í¨G\ÊLZY\ä\í¼\ô%’Álc»®ºC$Xg\ÊlR		W¹]\\_&=y*äª‘H†\æ•\Äb\Æú{H\Æ}\ÎÉº˜‰\ë]\çøÁ\Ï\"	Z£·¶»\âä‰“\ÅN%’Wˆ·wž8 ¶¶µH^t“%Š\ôy7#N\æ\ÊÕ—¤Á«OJEµXF†ŸA‰d¬¤Ú›‰$»2X\Édù?“ic…\æ­\×€¡#(yNF’\ä\Ê\È\Õb\Æ\ê\ç:ã§§`\õ±yc1›®³˜7\Åc\"‹I\õ¾4ü:D\Ï}\Üp¯)D´\Æ~Fr\÷YÇˆc\Ï\Ù\'n;\÷\Õ\â¸\ó\ö›\ÏH\Z‘<xP\ÌLj9˜\ï0!d¤4uQsL2\õÝƒ~¿\ág\"YWBI%,’ty°K,ž\Ûû\ÎGzMŠ~\ì5wþ1‘z\Ýy\0ýC\Ù$?\ãVÉ¬qò¥‰¤ËŒsœL‰–‰Y4”c“\ób\ÆûSÌ².íš®\ôDc6I\"v\îc„Ÿ±…H‚\Ö7\Û\ì>K{\ì›\Å[_ýjq\Þ~{³\É˜ÔŒ\è\ÙF+\ô\ÜûÜœÂ—ˆ>!’QHC\Ò*1‘\0\00~ø™Xˆ$h\ÍÄ–\Ó\Å\r\æ®\íožo½‚Ýµ]Š¤½\Èv³¿½]‘M¢\É1‹Q´ùý†ˆ$\0\0€a\"	²Ã¿þ‡D\ò­W\à\ë\Ú2h‘œÛ¹C	b“B}\0\0€I\Ð\Zwkûq¾G²5ƒI\0\0\0 IÐš»\ï¾N}\ä\Ä\Ä1\âœ}øB\ò@$\0\0ŒI\Ð\Z¾µ_¶\ÉD\0\0À(\0‘­H\æ\"	\0\0`€H‚\Ö@$\ó‘\0\00\n@$Ak ’ù”Hnß¾]\\\öOÿ$.½\ôR\ñ\éOZ\\rIW|\êSŸŸø\ä\'Å¶m\Û\Ä\ì\Å‹\Ë.»L>|ØŒ\0\0\0\0\â@$Ak ’ù”H’D>û\ì³Ey†\Ê3e¹ü\ò\ËÅDWJ&d\0\0@I\Ð\Zˆd~%’”‰$|Z¾.O?}D<\õ\ô\Ó\òuzZ|\ß\Éo~\ó›\â\Î;\ïŸú\Ô%f\0\0\0\"	Z‘\ÌÏ D’¶³•HZ‰tD\ò)%’\çŸ¾*3ú\0\0\0„H‚\Ö@$\ó3(‘¤\ÏD’HV%R‹\ä\÷¿ÿ”øž,GŽ<#.šù3*\Ä!13Yþ¥þ\ÙKýÆ¹©¯þ~:\0`\èu§\ÄÔ”.\Ó\Å\ïÝ­ˆ…é²¾\Û3\Õ>½n`¬¦Œ\ëþŒž%<¯$3\Öeaº¨Ÿš\êŠ\ØRu\Üp»Š1½ \Ï:N¥O\â\ÜÇ“D´\"™ŸA‰$\ÝXCŸ‹¬J¤,F\"­H^p\ÑEfTˆy1o\åQýNzG\Ö\ô»\æüùhý\Æ9\0cÁÊ‚X(Ìª\Ç~;¹\'z¶^\ö™\n\õ·\õ|¬<’Ò—”«Ä¼Á˜\Ñþz®¨\è*Œw»,6‡\â\É\ö¤Hz}œk\â®gü(ÿ\Ñ‘­H\ægP\"Iwg\ÓM5‰”¯••\È\ï}ÿûJ$Ï¿\àB3ª&”d\é\ÉC3“\ÈJ0Ô„„ˆD) `”‘cG;-²MvÏ…\Í\Éq\×\Ù\ë6•¸\ðy\Ð\Ý)†‰5û}üu…\×9h‰´¯;D´\"™ŸA‰$}\Å‰¤/‘e6\òû\â»\ß\Ó\"y\Þù˜Q50y¬ˆ£\'–\0€a£™0Z*\òdû©G\Êþ\é,UÝ–1Ÿ7\ZÓ¯³Ì†\Õo1Î2‹Ÿ\í:iN¾\æ@ˆ¤Á\Ë\ÌB$Ak ’ù”H\Ò\÷Dj‘”\ò\è¤)R\"­HžûÁ\óÌ¨0$ê³©$D€¡\ÆßŽ&9R‚H\"*}\ô\Ø\Ç67o\Æd\Ä\ã‘(¦²“¾H²\ÌfT$}<™M\ã¦Å¹VIŠH\Þv®8Ž\ãø\Ä]\É51(‘üø\Çg\Õ\ëQ\È\ï¿H-’G\Ä\Îý Uƒº¹F\"	À¨P#BžZ’\"\É\å\Ï?.¨Î›\ÉzaKK«+’\Î\\\\©>Ô¦3¡Ó¢\Û\õ\Ö=. #	rSˆ\ä\î³Ä±$¯>W\ìGF²ƒÉ~\ìc\âˆ|=|‰´©\Êw¿§¾g\òœ|ÀŒªg¾c\î\Ü\ö\ÄŸ‘`a·$h\ô±®F\"™7³\Í:¸H\Ò\órK¼(ŽL6\é£IÏ»¹)\å\"	2 E\òq\Ö1\â\Í;±µƒA‰\äG>úQ-’RyÒ–\'¥DR!‘|ÿ9\ÓfT€ùysg6Á\îÎ®\ÜÁ»¶:‚’\'\é\õŒp$TV\â\Øs/\ì£\ÐJ«\Í‹\ë\ÏQc\í¼!(^™‘t\à\ÙFš+ ‹NN¬ÿØ _c’lˆ$hÉ®8y\âdq\Î9\Ç\ß!xüŒH^£…bž$£úý‚”Í²cl6K\ÕM\Î\Ý\Ë§M‰‹~\ì¶\é\Ïùy±‹x<\Æú2(‘ü\ð?~D}þ\Ñ\È\ï\Êù¬DZ‘<ûý\ç˜Qœ\ëÿI\ìj0|”Û³eQ\Ù%%ee]\ép\\\éPJT¥„/\ZÊ±\ÑyU·j\ÌxŠYÖ¥]3§H\òy#1\Çd$AN¿NŠ\ä\rgŠc¤8{\Î>“‘¼Rœ\"O¹ÚŠ¤GþB’\æ	 	‰\ZSÖ“\è•Z\í¯Û¼z\ç\Ø{>9Y®eˆ²iƒ\É}øÃ®H2y\ôE\ò¬\÷½ÏŒ\0\0\0\Â@$Ak¶n³\"y²\Ø\É\î\Ú>pÁ\ñ\âø\ï*3’L\ÊH‹l\Ë`U²€\ê3w5¾\Ó\ñ>o\çe\ÅTQAI½ú\"n)ˆz\rL\Ç@$\ég\Õ\ïl7(\Ö\Ùf\0\0\0\"	Z£D\Òlm7Iý\óz\Êùy£zW\Þ\Ô\Í\Z²ŽdP=\ò½Rg,Ç—@~lž\Ó6{!e_½\Õ\í\Ë\çú3(‘¤Ÿ=¤_¬¡/§ï‰¤¯ø¡»³\é\Æ\ZúL$mgS&’$\ò\ï\Þ{–\0\0\0„H‚\Öl3wmo?9½µ]d¹\0\Û×¶Þ“:O\ö\Ê:‚\êC¿\ç\ìÊ¡{¬Ç„2”2º\Ü\ð\öøú2(‘\0\0\0r‘­)¿Gr»x³’4]ü›mhkÚ¶•‰E-oª~²£>³8s\ÈÔ¥n¶±\"ª\äÓŒ§\È2º\Ç\ô<ü9K72\çz‘\0\00\nL¼\á…/o¸x\Ù‚\ÍÉªXš›³³¼Ì‰¥U\ÓÜ’\Ê’W¾þ§úI\"	\0\0`˜x\á\ß\\ož‚Í‹\ÉEþ\ï…\åE)“‹\"\Ç?! ’ùH\0\0&‹\")rÑˆ\äò¢Ÿ­”enIŽjD2?I\0\0\0£\0>#9TErui®\"‹T7·†ý\îz‘\Ä/\Û\ôKn‘üú›Ï­”OŸøV\ñÄ¿¼[ü§)\ôœ\êB}\0\0€É± \ðI7=©€H¹E²\÷+[\åU¶|\èù¿.}\Ç\óBu¼-\0\0\0@ˆ\äXûŒ¤{\Ã\rDrx\È-’K/ýC\ñ½…©G[.ú\Ù\ã\Ä\áÿ\ó<§P\ïc\0\0\0b\÷ÚŒ¡\ÏH†·»!’\ÃAn‘üÊ‹W‰$=\Úr\Þs_%¾\ñ¿Ÿ\çª\ã}l\0\0\0BL¼\ð…#\à’›€H®.‰9d$‡–\Ü\"ùw?ùR§œ\ö¿(\Þ\ð#\Ïý\ÅÏˆGþ\ê\çT¡\çTGm~ÿÑ„}¨\÷e\÷\ë\Ã\Æ~iš\ÌkS?s\Zú•)û\Ô\ê0\ê\â€l\ôºSbjJ—\é…S»\"¦\Ëún\ÏTû\ôº±š2\î´\ðš\áy%‘˜±þ+\ÓEý\ÔTWÄ–ª\ã\Úc\õjž\éye\\b\õ\ã½>\ê{$\ñ@›Àg$e\ñ?&	‘r‹\äŸþ\Ùò»¯¿Z\ìþ\ÜM\âþ­G‰‡ÿ\ògU¡\ç_¹z·j\óûo<kŸ¹\õž¿Ÿùr­\Íüx€ú=ü˜\0\ò¹b\ó6‰²±² \nƒ\ê‰n!}=Ñ³\õ²\ÏtP´¨¿­\çcµTøbé˜73\Ú_\Ï]…‘\ân—\Å&b\õ!hNÙ·\"Œ±ú1ƒþF¦»øŒ$hD2?¹E\òÿ\ô:ù\ßc\Õ#•\ß8q§ø\ÆÁÄ½oü	\õúQ¡\çTGm¶Ÿ-\ÏZ\Ä\'—,­•\õž¿Ÿùr¯\âE²Á\Å/FÉžþ\ËV>‰8`@X•‚V\Â\åŽA™<fp”™\Ó\ò(û\÷%Vl\ÞhLŽ»\Î^7´\æ‘\óˆÖ—\Ð:º$K\îy\Å\ê\Ç\rû:A$Ak ’ù\É-’ox\Ó\Õ\ê3’\ôHe\ò×»b\õ¡Uqû‹\Ø\ô\êùc+«6\Û\Ï\õ›\ç\ög)©3\Ð?_\é\Ö\Ò2_þœ¥ÿ•ú\ç3@8?{Iu\Ô\Ç\Ë·g\ì\äÌŒžWMeÖ ž³Ÿå”¥©\÷~†³\ìŸ^»;¿ž\Ë9•\Ê\ï\Î\Ç\ç,c\Ú\ã\Ð5Š\õeÏƒ¯‰¤\ò\Z\ÔA\ñbý\è\\ù¼©xu\í ?Í„\ÑR‘<\ÛO=R–¶š›d\ë\Êy£1ø:MV\Ñ\ÌU•NNC‘¤9ùš)\ÛFkPY·\õcG)\öI\Ð\Zˆd~r‹\ä\ï¼nN‰$=R9æ¸‰\å{\ï7þ—ÿbzq\ãýª£6\ÛÏ–8±7~#*…<H!q$\Émý\ö¹>\ì˜6¯>ˆŽe¥K\Ë.Ÿ\Ç<\'asŽ\ÐbWýüž³~\í±ùx\ë(3uus\ò˜ü8\ÕFø}S¯	W¼)hLB\0™˜²SPd\ÇßŽ&©S‚H\")’}ls\ó\ö&\"GB˜\ÊN®E$Y\ö\Ó\ÆXý\Â\Î\"	Z‘\ÌOn‘|\é\Ëÿ\Ò)/ú…?Ÿý\ÌU\âÎ›\ï4=„¸c\ï\í\âÊ×¨6¿Œ\Ê6%É‘† \Ä\\ibmL8Š¢:¦ú\ñ :¶…\êŽa\Ï\ÍXGŽT]@`\õÉµ\Ç\æ7s:\ëU\í\ì¹#u\r\çtŽSmDª¯¬±s8k5…\Z‚\ç`¡x~Á».•¿‡DÕ‹Êž\'†–tF’\éZ@5\Õy\Ó\"Y³NIZZŠ$\ÃY¦Xý8Â¯D´\"™Ÿ\Ü\"ù¼\í¿å”Ÿ\íž ~\ä·Fœ\öŠÿ*þ\æWt¡\çTGm~ÿ ~f\Ï ;“K\ß\Ö\õ\Ú¥©ŠOOX\Ü1\Õ\ñv{¾”§À¼ú5‰dZ	­}4•\Í\çtŽSmDª/{Mb\×\"	\ÅqÎf„-\ñ8 \',³–€­â‚ž B\ÑH$#\ó\Æb¶YgA¿\"I\õ\å¶yQ\ä:¦ƒ\õ\ã(“\î5‚H‚\Ö@$\ó“[$\î’\äU¶üÄ©¿,\îù³\ç8…\êx[ª\Þ\ðIœ¬\Z—–tD\Å\Z¯o\ß/„k\Å\ÝZ/%§Ÿ­\í\ô\Ú\Ã\óG x“\Ñ)¤›H\Í\É%\\¢2À±s¬\ë›zMB\×\"\ál-ü\ïB\Ú\Øþz	?AÉ“\ôzL¬H¬Ä±ç”‰+,\ÒG	 •;V›73ÖŸ£\Æ\ÚyCP¼\"Is…¤0–yçŒ¤w­ ’ 5\Éü\ä\É\ç~\ä\×\Ôg$\éÑ–ûK\ÅÁ“r\n\Õ\ñ>¶ø8[ŸJ´¸\èc.GZ\ôM)º½›L(©1q¨˜\ÎÅœ\å\à*J–t¿\è\Í6¬»EK}l½/r¶ž¯5°\ö\èüq\Ôyù\çS\Â×¯¾.§l¯\\£h\ß\Ôk\"‰¼q(^D$%ZªýX\ëW‰eüœ¬š,*¨¤¬¬+ŽK\"J‘¨\ô‘\ð\ñEC96:¯\êV\ïO1Ëº´kB$s\ã”\0\"	Z‘\ÌOn‘|Î¹\Ç*‘¤G[~\ì-/w\ôS\ânS\è9\Õ\ñ>¶´#$ÀB\òW\ëi\0\00¤@$Ak ’ù\É-’ÿ\×=¿R~øWJ\\\õšŸ7…žS]¨o; ’Q(\ó\ç|®\0\0Fˆ$h\Í\Ä\ÄV\ÑU\"¹]¼y\âXq\îm¾H^\ÃD‚K=/·ºœ\í\Ò1O\Ñ\äÉ‡z¨UiD²Šý\0®\0`´H‚Öœ¾e‹8\ó†~EÒ»À\â‘[$\0\0€A\0‘­Ùº\Ínm“H²¬¢,§\\\ÉI)‘•»B›  ’\0\0\0À°‘­Ù¶uB}\æ\rÕŒ\äU§ˆ‰\ã/wUDRJ\ää¤»}­\îµwkR¶\"	\0\0\0;IÐšþER?§\ÏDYI\ÊF¿ƒp<H\0\0 ’ 5[N7·¶Þ•º\Ù\Æ\Üpü\Â\ñ\"	\0\0`€H:,‹\Å\ÙY±¸l+\è\ö¹¥Us#gyQ\Ì\Êz[\â\óXV\Å\Ò\\\Ù\ß)sK²u8À\×ÿ\äg\Ð\"9·s‡x\×i\ïH–¥}·˜\Þ\0\0\0@ˆ¤euI\Ì\ÍÎ‰9)n1Á[^”9\'û¤D2\Z‡\ärNCU¿EY›B‹dPH!’›šA‹$‰\â\ÓO?-I\0\0\0M\"i²^{\"qŠ‹Îº\ÙY)W¼ž‰“‡)\ç\ô\Ús®.\Í\ÚiŸC\âZ`Îˆ¼-/\ê8t\ÎA‘$y“\r´Ž”H\Æ\ã\Ðu\ásû\Ç!\ôú+ë©ˆdìš¯\ÉüƒH\îÝ»2	\0\0 I)’¾€(!“\õA‘\ÔcªB\å‰OE\êB’S¥¤Ñ›·3Š\ÙT$ü8\ë	\ÉRú\êD\ÒŠCuv=\ê«yx\×\Ó\âˆdêš¯\Éül´H\î\Üq¹\êc\0\0\0Âˆ¤”±¥EG”-qic\ÄdÅ‘<‚KN@úˆ`,7Þ—\Åq\æ\Ä\ä\ñ2‰$¯k#’„H)\èMb\è\ó\Ä\á\"™¼\æ\ëD2?¹E\ò\Äw\îGt}´¼\æ´=A¡¤\ÉC3“\ì\Æ*û\ÕM!\ôW>•}‡ì·¥\Û|K\0û\îS\ç{Qc\õ!\"}ù/=­%†ûúØ’zÀ8\Ñ\ëN‰©)]¦VL\íŠX˜.\ë»=S\í\Ó\ë\ÆjÊ¸\Ó\ÂkR„\ç•Db\Æú¯,L\õSS][ªŽh\Õ{¨y¦\ä•QGÍ®Ï¸°² ¦\åu(Er•oµš\çI1T¶V\rT_l±–EKM@úˆ`,_†\Ø\Ú*\"Yo_«,`¤-DE\0=\å\"i¥Š/†U‘¤s(û\é±\éµ\Ø\ós\ãHø5K^\ó\õ\"™Ÿ\Ü\"’G¿„$’JL$Itš	!¿SŸIz\ê„\Æ3”\Ð\Z\íy°\õ:ß‰Zw\ñ3\ÅZc\ËZ!\ã€…B‚z¢[H_O\ôl½’„hQ[\ÏÇ’›U\Å\Ò!1o0f´¿ž+-rFúº]›ˆÕ‡ 9e\ßB$›\\Ÿ1‚®|˜H–’T\ÈRL$û­WDD’\ÆT„\Ê\ËHr™«ˆ¤Ó\Çû\çrq0&ª²D\ÏSS\'¤DU6}\Zˆ¤s=6ˆd~!’_û€\Øy\Ó\Ã\âMgßª\êè‘Ž©ÞŠ\ä	\ÛW’É”\Üp|¹©#¢IŸ\r†„˜™´5_Ø’‰\áR\óýbp\Ù€CbU\nZ	—;e\ò˜ÁQ\ÆNË£\ì_WØ¼Ñ˜w½nh\Í!\"\ç­/¡ut¤,Ï«~ü¦G¾n\ô:9\"©¥dQ,:\Ç!IÑ‚\ãg\ál}XŽ\Ø<\ÕX*[W\Ì\ës\Öˆ\éÈ¢·§-L\Ü’]CP$¹™,«u…\æ\õ\Öo\á\"\ëC\ð¸±\ç€H\æg\"ù–ow\Üÿ„xÏ¥U\ÝùW,‹\ÝS\õýg$\Ù\÷~\Ê%…\'…$>\ö\Ë\ç	•Á\ã[¯Ô¿Œ­%É¯\ð¦\ÊX\Â\Ì7C™O\Ýf\×G’e\ëTQ\Ü\õ\ñ-e.h>a3B\ç×‡\ÅN‹á’–ÀF1d]l\r`\Üi&Œ–Š\ä\Ù~ê‘²|f\ë·V*\Ëy£1ø:MV\Ñ\ÌU•NNLø¼zš“¯\Ùd\Û\Ôc\è\\\"\×gœ°YaW$%$@\áìŸÞªµºR®\ÜúRž\ÒW e¨\ãIR‹\Õ\'SI’ž\Ó9‚µ\Å˜HJ” ³s(\âD\ÅNŸ¥\ÞI\"r\Íy\Ü\Ø\ó@$\ó3‘<\æ\Ô]\êùµû«BIP½É—±\ß)q‘\äx¢X!$†ol!<\Õú°`\ÅÆ²yhlEÄ¨\'ž6NA¬^8g>-À1‰k\"\Î/@¨Q“\Ñc¿MR§-\"II‘\ìc››·7\Éx<\ÂTvr-\"É²ŸžH\Ö]Ÿ\ñ¡¼FR$‡™¦\"6ˆd~\õ\É\ë¸v{›Žm\ÏB\òR/’u²Ã„\Ìùü \Ä\É(r\Ñ\ô$\Î\ôs\æh:¶r¬\×[º–×®D\Ð\Æt\ÇqRGmv|§\ã\õc¤%0-¡–Z‘¤\ëÄP\è¬^T\ö<1´$E’\ËU@5\Õy\Ó\"Y³NIZZŠ$\ÃYO*#™\ØM».I\Ð\Zˆd~%’”‰|ü\É#…T\Ò1Iûœ\×5É¸«¸¢æˆ/–Uù#¬ ©¹\Z\rˆ¢³X\Ö\îÄ¬\É\äyq*BgH^›hŒ>²ˆ5\ë \ã\èü`La·$h\ô±®F\"™7³\Í:úIª/·Í‹\É\ô¼›.\ÛC.’`€H\ægP\"™*<\ÉK­H*ùJIOJ\ì\èy(\ë\æ))E©\éX>_>Y;I™ýüf\Ýy9\Ò\é\Ïi\à\ñB\Äbxr˜$¹lkƒ\0AÉ“\ôzL¬H¨¬Ä±ç”‰*,\ÒG	 •,V›73ÖŸ£\Æ\ÚyCP¼\"Is…2<#½>\ã†{\í ’ 5\Éü\ä\Éü\ß#I\Âb·S\ÙH¢*Y$ƒ®°•±¬@Q&¯8&±*ú0Ž\õ\ç+‹˜¶¨5\ðþz;Y·uD§N\ÂØº\ÊkÀ¯/­1\Ô\õ)b\èRfFp­¥Á\ZÀXA\Ù$?ã¦²KJ\ÊÊº\Ò\á<i\"\éª\ô‘\ð\ñEC96:¯\êV\ïO1Ëº´kº\ÒS\â\Õ7\É\è\õ/üŒ-D´\"™Ÿ\Ü\"\éCr’\ÆPi²µ\r\0\0`<\ð3±I\Ð\Zˆd~FS$y&Î–Í\r\Ëq^\Ã\0\0\Ú‘\ÙÙ”\"i·LSŸo ƒÉ¹;” 6)\Ô\0\0\0‘­\ÙT\"¹Ái´H\0\0\09€H‚\Öl‘\Ô7Z¸7+lI\0\0\0£\0D´¦\"’·+Ž+>\ÃuŠ¸F‰\ä\ç\õç»¼LŸ¾;\Õ\ÞKŸ\ßm[m³x\õ\Î]¼‘Ïywúºw\Ûv\Ä»cV\ß)\Ë\î\ä\r®Aœ\×_¿l\ëÌ°X¼¿\îkH\0\0 ’ 5®H\îoxµ8o¿\ÉH^}Š8þÂ»ŒHNŠI\ç\ëT¤ Ñ¯~8²\Å\Û}\ãm–DŸù\Ð\ïS&J\0\Í#ƒ\å¯o£5Ð¡ÿ3¡L§K[ ’\0\0\0Fˆ$hÎª$¶“H\î;G¼Z³\ò\ç\×\"93Ã¾hY	\×*’)ol¢M‡aB\æe\ZUq\í\Í\ôq3•\Å/\Ú\Ê/¿&ü5˜¾\Ñy\õ\Ú&¥D†…\Ö\É\òŽI\0\0\0£\0D´†2’Ý“&\Ä1g\í6\"ùVqe\å3’F$UvN\Ø|‡Ž¹P…\ä*\ÒF_À\ì™t@+¤DRÅª\Ér\r4NµE\ç¥þ²\Ï\ädUh½X\ö\Ø2h‘lr\×\öÒ¾[Lo\0\0\0 D´\ÆIµµ=!Ž;oD$­œÍˆ\Ë\Úi¡\n\ËU°-$’\êy(û\Ç\Ñ}\n¯\ó$°C}\ä\öu\æ\â}c\ó–ýÝ¸„\Ë[-’$Š¡ïŒ´2	\0\0 	I\Ð\Z½k¶¶+7\Û\ÈÂ·¶•8i\ñ*³€¼¾*W|L36\Æ\ßf®d%N>\á\ÎS•¿²Í¹™\'8/_›¹a§¸\Ù\È[·‰m‘Ü»wd\0\0@ˆ$h\Í\æùúŸ\áa£Er\çŽ\ËU[\0\0\0€I\Ð\Zˆd~r‹\ä‰\ï\Ü+Ž:\éúhy\Íi{‚BI%,’~v–g[‡~\ölnü¬¿%V?^\ôºSbjJ—\é\â\÷\îV\Ä\ÂtY\ß\í™jŸ^70VS\ÆuF\ÏžW‰ë¿²0]\ÔOMuEl©:n =Voˆ\Í]ÿ8²² ¦\åu€H‚\Ö@$\ó“[$C\òè—DR‰‹ä°¿»kT\ßY:t²D2Š€…Â zì·“{¢g\ë•$„D‹ú\Ûz>VKVR®\ócFûë¹¢¢«0R\Ü\í²\ØD¬ž›7±ž±„þF\ä‹\0‘­H\æg\"y\ñµˆ7=,\Þt\ö­ªŽ\é˜\ê­Hž°}\Õ)›I$!\ãD²$V!!\ârÇ L38\Êjy”ý§d´¦°y£19\î:{Ý¦9h½O\ìú\Ä\ê\Çùº\Ñ\ë‘­H\æg\"ù–ow\Üÿ„xÏ¥U\ÝùW,‹\ÝS\õY3’ÞGú~\'þ\ë@¶˜›•‚ý	šƒ\õ\ç\Ù\Ä\èŽ¿F\ïØ‰aoœ\Ê;FÿrSº¿\îS\Óþ\å—C1B}ü\ëœ#nj½¼¿?Žˆ¯Ç½–\×\Ý\Ë\'¯S\ðÀ]w‰W}MYü\èßž\÷šÎ—mÎzu\çjË†dÌ›	£¥\"y¶Ÿz¤,Ÿ\Ùú­•\Êr\ÞhL¾N’83O\ísC‘¤9ƒkn8~±Yaˆ$h\rD2?ƒ\ÉcNÝ¥ž_»\ï°*$‘\Õ[‘|\ÙûÒ¿H\ê7\Æ\âR½\ò~þ¸TÞ—ž»o\ò\ñ9,\î\\\îÖ¶\Û&­„}•Å\×2\ÆBBŠ#Ÿ\Ëz\÷×•b‚Ê¡qt.~Ÿ\È<­\âz\Ïùz+±ü\ã\Äy×¼\î\é_Á\âøsZ\ô…¤9Å«|M\éy\ä\Ú9ýe\\û\÷U9Ÿ~ÿ\Æ\×;ºø\ìa@\"‰¤Hz[\Ï)Á\ã\íMD2„.•l\'’±y\ë\Îo\óSfd!’ 5\Éü\ê3’\Öq\í\ö6\Û6ž…\ä¥/‘t„EC™£\âM\Ô—\ì¯ß€í›¿ûFœš\Ã\âŽ/³Gƒ·É¢ø\çÅŽ“c¼z\Ãf\Î\Ê\õ•1\õºý9\ì:ýµ0\è{T£\ë\rŒo·|^Yo%V\è¸n=\Z\÷u—ý’¿‚¥\ëB×»\Ä_‹\Å_‡aJqþe]Fº¿;Wq>µ\çZ\Æ*\æYtV/*CžZ\ÒI¦k\ÔT\çM‹d\Í:%i©[kF16oýz\Æú|¤oˆ$h\rD2?ƒI\ÊD>þ\ä‘B*é˜‹¤}\Î\ë6V$m_–Ùª\ÃY#ˆ¡\ñÇ°ãµŒa\Ð\ZlmƒªE»ý\Ý\í\ðj\"|\è\Ð~Q¿:\È7µ^o~ÿ8¶žF¯;½\æºO\åW°œ\ñ<\ë\É\ñ\×fI¯C\ÃÇ¦ÿ\ö4þ\\4ÆœO£s¥\ç±\ó$C\õŸ\ï#A«¸ \'ˆ…6\ÉÈ¼±˜m\ÖY°‘Œ\Í\Ûl=\ã\0—ˆ$h\rD2?ƒ\ÉT\áYH^\Úom\ó7Q\\ª¿ÿ&\Ë\ß|SsXü¹8:†;Ž?†¯eL‰+’\\\æx}žŽpzqt}\è\ZÉ£bu”).=­×\å\Ç×£cÖ½\î$¿Á_Áâ‚ª\Æ\ò5XÜµ”T\×Q®\Ñ\ÂûTÿ\ö\ÂýY}\å|\Ö\ò7\Î\×zÞ‚ \äIz=&V$ZVš\Øs\ÊDé£„\Ë\Ê«\Í‹\ë\ÏQc\í¼!(^‘¤¹\ì\Öv\ôú4X\ÏX\à^;ˆ$h\rD2?¹Er0\ß#yCSo”±\ÌW`\\´?\õµ\õ²\ïÄ’\ä–š7]\'†\ï\ÍY\ó\Æ\ã¯[“H}\Ì\\X°TÿHFQ£\Ç1‹BŸ)”\ÅX\"G\\:o\ÝB\Ëk)Š­G‘|\Ýyü\\™ø4v²£>·YŽ·x\ó¤\Ö!K\è\ï ú·g\Ût\ÌN§\Ìú\ò!\ésµ\õ²ƒø\Zc\Ï\×e“\ì*\Î\r+J\ÊÊºÒ™˜Ü©C)T•>>¾h(\ÇF\çUÝª1\ãý)fY—v;O¼z&’±y“\ë#øµ§‘­H\æ\'·Hú†¤1T\Â\"9NÐ›·\Í m4¡µ\äXß \âŽt­\Ú\0£€\ó\n	D´\"™ˆ\ä01LB5(\áT\Üq®DŒIˆd~-’s;w(AlR¨/\0 DŒ/I\Ð\Zˆd~-’\0\0\0@ ’\rY]š³³³¦Ì‰¥U\ÓP°,e\Û\â²9±º$\æŠ‹r„\Ç\òb9G$Pr‰ø©qË‹¶Þ”\äITH\æ\"	\0\0`€H6É•’²¹%Q¸˜¸917—\ÉU±\Ä\ÛI\ZYŒJ\Ì\Éu$\â×Ž‰qs&’t§£½\ë“? ’\0\0\0Fˆ\äZP\âXfü–µˆQf/*’4\ÆE.pk”9¾Žd|gý\Ô/\íƒAf$ù—(;_§±ÉH\0\0 ’kÁ\Ë&Z’\"Ic¼Æ¢¿‘À%¶\Å<\×\Ä*ù:R\ñ}œ\õ\ë-ùrk»¡\Å\Öv~ ’\0\0\0Fˆd\ß\Ä3}kIj“W6“\Ü\Õ	·Ž\Æ\"Y“ýTk\é/C©D\ò†3\Å1\ì‹u\ßv¥É«ÅŸO/.:hE’\ß\Ý\è\Þé¨³M\Ú|Ø—«Ì¥{¬‹ù\Z\ïË„\Ý,§?.6\ß\à´H6¹k{i\ß-¦7\0\0\0\"\Ù$aqYl%’^†3+´ŽF\"™^¿¦I—»\ï\Þ&N’\âu\òv“‘¼\í\\q\Ü\Äq\â‚ýˆ¤|>9)%¯IG\Ë_\õ\'\Ëƒ c&J*y;\Å\nÍ¿þZ$IC\ßid\0\0@ ’©¬¤ü¥>\ÃXiKÅŠ¬£\ö3’M\ÑW\Ï\Ý×.Žž8Ilg[\ÛW¾mBœr•I)oŸO‹$ý„[g¾iC\É`\ìK“½1¾:¶9Pým{d¾ubDr\ï\Þ=I\0\0\0I ’h&aùS7µ\Ø:/†“…\Ôm\Å\ç\"\Õ8&™±\õ\ñƒ\ãVWMC ;ZGZ$ˆ».<žm\ó-c#k\óR\ð”\ÍqyKµ1rŠ\ä|§\æ\÷ˆ×É;.W}l\0\0\0B@$›@rUÜŒR_\Ì\Ò\"I\ð[ü¬Ÿ{\ÓK1†Ç¨]G$~jœ‰_\Ö\÷wxkûm\âª\à\Í6¾,Ä²¶\Óvk»K’\Ê2Nl¾\õ!·HžøÎ½â¨“®–×œ¶\'(”T\Â\"i_V†\î\ë™ü5n\Ü\ë	6‚\Øÿ†7\ö\Û\ÃB¯;%¦¦t™.~\ïnE,L—\õÝž©\ö\éuc5e\\\÷g\ô,\áy%‘˜±þ+\ÓEý\ÔTWÄ–ª\ã\Úc\õ†Ø¼\Ñ\õ#+bZ^ˆ$hM\õf›W‹\ó\ö\Ç\î\Ú\æÿ\'®\ß\è\Ã\ò–j\ó\Ñ}­0¸[\Õ\Þ%¶¯m37\Ù8\"”šo\ð\äÉ<ú%$‘T\â\"¹q×§\î\Z\Õ\r[c\ô]¤ \ö7:\n»F\nÀBaP=\ö\Û\É=Ñ³\õJB¢Eým=«%+)W‰yƒ1£ý\õ\\Q\ÑU)\îvYl\"VÏˆÍ›X\ÏXB#\òE€H‚\Ö\à\ë\ò3‘¼ø\Ú\ÄÎ›o:ûVUGtL\õV$OØ¾\ê”\Í$’ˆq\"\Ù«q¹cP&eµ<\Êþ\Ó2ZSØ¼Ñ˜w½nS‰‹œG´\Þ\'v}b\õc„|\Ý\èu‚H‚\Ö@$\ó3‘|Ë…·‹;\îB¼\çÒƒª\îü+–\Å\î©ú¬I\'\ëk3\ÄþW+Q1+\ö\'hÖŸg£c8þ\Z½c\'F\ì&«vcø\ê\Çúû_mE±(\Ç\ð¸Š\ê\ã_\çqS\ë\åýýqD|=\îµ¼\î^\ö8y‚\0\îºK¼ú\èk\Ê\âGÿ\ö¼×”>\ÓmÚœ\ÛÔ«-’1o&Œ–Š\ä\Ù~ê‘²|f\ë·V*\Ëy£1ø:I\â\Ì<µ[\Ì\rE’\æ®¹\áø1\Äf…!’ 5\ÉüB$9u—z~\í¾ÃªDToE\òeg\ìwJÿ\"©\ß‹7J\õ\Êûù\ãRýy_z\î¾\É\Çç°¸s¹[\Ûn\Ýh¥\ßø½z\çx-c,$T¡8\ò9ÿj+u.1A\å\Ð8:¿OdžVq½\ç\ÎWqù±ü\ã\Äy×¼\î“\Å8B\Æ\éÄ¾ÌŸÓ¢\ç($\Í)\î\\\Å\Ø\àkJ\Ï#\×\Î\é/\ãÚ¿¯\Êù\ôû7¾~ø\Û\Ñ\ÅgI$E\Ò\ÛzN	oo\"’\ñx$t©\Ì`;‘Œ\Í[w~›Ÿ2#‘­H\ægPŸ‘|\ð°Žk··\éØ¶\ñ,$/}‰¤#,\Z\ç\Îx\\²¿~¶oþ\îqj‹;¾\ÌIT\Þ&‹\n\àŸ;NŽ\ñ\êY›9+\×W\Æ\Ô\ë\ö\ç°\ë\ô\×Â oˆ®70¾U\Ü\òye½•X¡\ãº\õh\Ü\×]\ö›±k¡*¶76­5p½KüµXüu\Ø¦\ç_\Ö\Ùe¤û»s\çS{®e¬bžuAg\õ¢2ä‰¡%‘dºAMuÞ´HÖ¬S’–ºµfc\óÖ¯g, \ÏG\Z\ñ†H‚\Ö@$\ó3(‘¤L\ä\ãO)¤’Ž¹H\Ú\ç¼ncE\Ò\öe™­\Ú9,‘5\Z;^\Ë­\Ñ\ÉvE¾\Ú\Ê\Ý¯\Æ!\Â×ˆ\ã_aµ\ö¸©\õz\óûÇ±\õ4z\Ý\é5\×}\æ;tÏ³žm–\ô:4|lúoO\ã\ÏEc\Ìù4:Wz;A@2Tÿù>´Šz‚XH`#‘Œ\Ì‹\Ùfk\ÉØ¼\Í\Ö3pù‡H‚\Ö@$\ó3(‘Lž…\ä¥ý\Ö6\õÇ¥úûo²ü\Í75‡ÅŸ‹£ch±\ãøcø\ñZÆ”¸\"\ÉeŽ\÷\×\ç\é§G×‡®‘<*\æPG™\â\Ò\ó\ØzýX\îq|=:f\Ý\ëN\ò«2‘ª#\ÏU\åk°¸k)©®£\\£…\÷©þ\í…û³ú\Êù\ôû7>`‚’\'\é\õ˜X‘hYib\Ï)UX¤.+w¬>6o,f¬?Gµ\ó† x\rD’\æ²[\Û\Ñ\ë\Ó`=c{\í ’ 5\Éü\ä\ÉÁ|d\èMZ¢\Þ(c™¯À¸hý\\d\Ñø;lrKb„\Ã\Æ\÷\æ,ŠyãŽ\ñ×­I¤Š¾Nf.,Xª$£¨\Ñc‹˜E¡\Ï\Ê\Çb,‘#.·n‹!eµ\ÅÖ£H¾\î<>—8[o\â\Ó\ØÉŽú\Üf9\Þ\â\ÍWZ‡,¡¿ƒ\èßžm\Ó1;2\ëË‡¤\Ï\Õ\Ö\Ë\â\Z”M²7ª87¬()+\ëJgbr§¥PUúHøø¢¡Wu«ÆŒ\÷§˜e]\Ú\í<a,\ð\ê™H\Æ\æM®Œ\à×ž\nD´\"™Ÿ\Ü\"\éCr’\ÆP	‹\ä8Ao\ö6ƒ´Ñ„Ö’c}ƒŠ;.Ðµ\nI+\0›\çˆ$h\Í\ÂÂ‚ø\â¿(v\í\Ú%n¾ùfqë­·Š^¯\'\î¸\ãq\àÀU\îº\ë.%œ(\ébH\Ã$Tƒ¾A\Å\èZA$Áx\0‘ÙH\æ+–A‹\ä\Ü\ÎJ›\ê\0H‘\ãD´\"™¯X-’\0\0\0@ ’ 5\É|\Å‘\0\00\n@$Ak ’ùŠ\"	\0\0`€H‚\Ö@$\óD\0\0À(\0‘­H\æ+ˆ$\0\0€Q\0\"	Z3”\"yÝ»Å–-\ï\×ùÏ‡ \\\÷\î-bb\ë6Vwx\÷ý…Ä–A‹d“»¶—\ö\Ýbz\0\0\0a ’ 5Ãš‘T\Âf~1b\ë¶pŸu/¾\Ô\Ò1[Ÿe\Ð\"I¢ú\ÎH[ “\0\0\0š\0‘­Á\Öv\óBr»\å\Ý×™c‰\ä’k‘Ü»wd\0\0@ˆ$h\Í\Ä\ëÞ§D\òü7²ßŒý\ã2‘ü·b\ëV—-\â\Ý×‘8m[‹\ç¼ø\õü¸\É·\ÎL†\ÆP¡¾\éuUÇ—[\ÑT´ú\ó\Ë6gûÚŽcqT6r«\Ø\ÆúX6Z$w\î¸\\\õ±\0\0\0‘­©f$?,þx\â\â´y.’!Is…­,~}¿c¼\çr\î-Á1¶¶š›Ž\×Yfm±cªYF·\ÇÀg7-¹E\ò\Äw\îGt}´¼\æ´=A¡¤\Ò\\$\é\×=JÁž\ØL¿\ô1\ß)\Îk’ŸT¬ž\é3ß±×©¿±‡f&‹º²„~Þ°zý\õœø D¯;%¦¦t™.~\ïnE,L—\õÝž©\ö\éuc5e\\\÷g\ô,\áy%‘˜±þ+\ÓEý\ÔTWÄ–ª\ã\Úc\õ–\Ä9ÖŽVÄ´¼>IÐšB$\Ï#{c\ã\"9\Ë\Ê6ÛŸ\n\ï\Ã\ë©\Ä\Æ\Ä2‚úù¶­\Ô\ÎÛ¼²m«\É6\È\"\ê¢ûl	J&\ïã‰¤Ë’[$C\òè—DR\éO$KIQ\Â39#F\ßYè¼¬¨±s<4#&C\õ\ñ±3…ù\õ9Öƒ®sUDý\Õz\é3\á8`Œ°PXPývrO\ôl½’„,Q[\ÏÇ’_¤‹“˜73\Ú_\Ï]…‘\ân—\Å&b\õœ\Èz\Z#\èoD¾I\Ð\Z%’—ý¥xù\ÄÅŒ\ÊH~Nü\í+˜H\Îþ‰˜(2oaa#‰\"i\Ó\æÖ§\Æ(Œe·IQ«H¢[´(²1u\ã“\")×¿Å¿#\Û\ï\ÃÇ®\ßg$I/¾\ö±\ó¦‡Å›Î¾U\Õ\Ñ#S½\É¶¯:¥H¦\äg¤ ¬`§°¾B\Ü|\n]d¬\Ë!13¸N\Ær\Ù\äø×ž\æ˜ùMòš€Œ•‚V\ÂeŠA\Ù8fp”\Ô\ò(ûO/\ÈhMa\óFcr\Üu\öº¡5‡ˆœG´^R»ž\Ä\ØqB^\'º.I\Ð\Z%’x½˜xù©\â\n\ÉÏ½C¼‚e$gÿ„qÁ\ÈR@ØŒ\à\åI?‹\É\ã\ÙB\õVìšŽ¯\Û\Ú\æ\çÁÛ©xŸ‘¤B\ë/²ªƒÉ·\\x»¸\ãþ\'\Ä{.=¨\êÎ¿bY\ì>\ð˜ªDF²r\\dÄ¨\Ä2m\íÆl\ÙLu¬¿\îS\ó-\æP¶®\"pF\ðüú\è\ÅÆº\Ðúª2\Øh¬¬\ó\ç\Ôx×¨\Ë\ë\é9;w–=v®I1§\Ó?v^+’VSŸ˜Í„\ÑR‘*\ÛO=R¦NoO\ÕJe9o4¦_§\ÉÆ¶žb\Ò\ç\ÕÓœf\Í\õ\ë‰\Å/lV\"	Z3\ñÒ·‹Ë¾x™8\õ\å\æ\â$þXe$\ç\Å;_)_ù.±PÜµ6[BRW7†×»}J™\ó\ã•}\Ê8¶\Ð\Z\êÆ»c«M-›e¶,\î]Û¦¨,§Že„Hs\ê.\õü\Ú}‡U!‰$¨ÞŠ\ä\Ë\Î\Ø\ï”6\"I\"TJƒ\'…\0¥\äd-c,<\Ë\çÅ”\õ“\öX\ÉOLP5Q¡£\Çb¬\ÎøùR\×DI\ÚüqDý\ØH&S\ás£\çU™\÷\'ü6&\êº\ö3\Ø(ü\íh’(%h‰$’\"\Ù\Ç67oo\"’\ñx$u©\ì$Dr0”bˆ$h\Íh~ý‰Ÿ¿Eª\Ë\\7\Ø\ðb\Ôg$<¬\ã\Ú\ím:¶m<\É\Ë\Úo¶a\Â\àe«TQ\ÖÁ%ƒ`\Ç\É1^=‹a³i¥s•1©\Í\Ù\Þm#’%\ËfþN\Ç\ë\'I\Ë`X>-µ\"Ik\ç\Ç\î9—qø9\Ò\ó\ò\Z:¡h®¢-\Ü\ßis®£F_k\õ,>\Ø@tV/*{žZ’\"\Ée«\"_–\ê¼iq«Y§$-­\rE’‘l\0}>Òˆ7D´\"\Ù_Q_\'ù¥eP\"I™\ÈÇŸ<RH%s‘´\Ïy\ÝÚ·¶\Ñ\Ðøc\Ø\ñZ\Æ0J2\í\óV¼\Üþ¥21\âxW<C)NŒ\è\ØT6\ÑP3/W\æ+`\ç\ìl%\ós\ç\Ï\Ùzœ\ë\Î\×\é^7\ç¸V$\ó€\r¤\Ì&¥ A«¸ \'U…t5\ÉÈ¼±˜m\ÖYÐ¿H\Æ\×cH\òk‘­M‘\Îb”H¦\n\ÏB\ò’E$U[(û–“5)qE’K\"\ïÏ³‚\á8®$Eú\ô…¶\ñcc=I,i0VQ\'d\Ô?”\äqøs}T_~.j\r¡þ„‹\Í];›lAÉ“\Èÿ\ß.kI–¬Ä±\ç\Î\ÝÜ‘>&‹¨§`\õ±yc1cý9j¬7\Åk ’4—ý\\g\ô-±˜\ã‚{þI\Ð\Zˆd¾b\É-’\ë\÷=’\\4<”\\\ØÌŸ,\ÚZ”€”A[Œ„DÇ„…†\ä±\è\ëˆR¯\ìsœ’+·” W\×[i\"¼8±nT— \Ì\ç%¨Ÿ\ÓÇ¬\Í$\á\ñM[Š¾Z\öT\ÝdG}¦´\ìÏ¯w\ì¼V~?[/KeM`½¡l’½QÅ¹aE	TYW:œ\'S$]•>>¾h(\ÇF\çUÝª1\ãý)fY—vÍ˜\ôy\õ\\$‰\Ø9*b1\Ç~\í©@$Ak ’ùŠ%·Hú†¤1Tš‹d.H<R’\0\0`£\ð3´I\Ð\Zˆd¾bv‘t2Lª\ä?ˆ$\0\0+Iˆd¾b´H\Î\íÜ¡±I¡¾\0\0\0@ˆ$h\rD2_±Z$\0\0€@$AkH€\î»\ï>\ñ\È#ˆo}\ë[\â;\ßùŽø\îw¿+žz\ê)q\ä\È\ñ\Ì3Ïˆü\à¦7hD\0\0À(\0‘­H\æ\"	\0\0`€H‚\Ö@$\ó‘\0\00\n@$Ak ’ùH\0\0 ’ 5\ÉüJ$¿\Óû\ñøm¯\õ\õ\â\ÛTn}½xl\é\÷u\Ù\÷ûb\õ–×©\ò­›_\'¾½ÿ/\Í(\0\0\0 D´\"™ŸA‰$I¤8|™,—\Ê\Òâ›—\È\òIY>!\Ä7.–eVˆ•\É\òQ\ñ\è\Þ\ß3£\0\0\0€0I\Ð\Zˆd~&’_%‘¬—H±\ò\â\Ñ=I\0\0\0i ’ 5}‹$ý&¯ý}cþ|P¿y¬~û\×û=`Y\Ê\ßfv¡\ßgŽµ\åbP\"I\Û\ÙM$R<\ò!q\"	\0\0 ˆ$h\ÍZ2’J\àŒ°)\Û‰%‘œ¥\Z±.î˜™\ä}\ó30‘¼UŠd‰üƒ8ü•\ß5£ªLs\é¶%,\Øþµ6šÿ#¢ža?W\04½î”˜š\ÒešÿÞaeaZLM/ˆj‹¤×Ž-\ãº?£g‰\Î‰\ë¯\Ögê§¦º¢g\ê+¨¸¼}E,L—1»Ñ’\ÊXI\â\ÜÇ‡ž\èšk@\"	Z3ª[\Û$³¥0€D3\ö›\Ï\óˆd\æaP\"I7\Õ4‘H\ñ\ÈEâ›»\ã\"Y\ÒDœFA$ùú\èX\n\åš^\ßØ¹û5\0c\ÅÊ‚X(ìˆ¤À—>#\nA‘¤6+W\îX’¾¤\\E\ç\ÄL¬“\æJJ \Æn—\Å&z¢gdüi_‘±Nw=\ã…{\îIÐš‰-§‹”Hnož8Vœ{›/’×°7Q\÷\rUg&ý7X\Êø¹¢	+tJ\î\Êú\ò½Þ¼ù{\Û\ä\áø„ŸU½\Ñ\ëu¨9Hy\ìo\ÉV$\ë%R<|\á‹¤$\õˆ$±s\ök\0\Æ’&Wˆ(\Û\×]\ÒI\Ê\È1ƒ£¾Z¥\\\Ä2˜AØ¼Ñ˜w½nS‰#\é	\É\"‘j#\Üv]\áuŽI™­[EwM\")ŸK™›Œ¾Áúo¾t\Ì\äQ½Ù»q\'9”\"Ø‰Å§þ\\ü¹ˆ„HV\Æ\çe`\"¹OŠd‰Ÿ/¾¹\ëµfT\n\ïº9¢o¯O“>V?93\Ã\Æ\è\ñùZ\Úþ\Î\Öz\ña\æ™/\ãPÿE\ó­w\öÚ«\ÃÐšu[\÷\å±\è¹l\ët\ô£-6¨“\Í8A&Œ3žLQÖ¤ŽbX‘\'+\ê‘2xfË³V*\Ëy£1ø:M\Æ\ÐÌ•–9\ïü8|z^Y³;\"i¡\ë‘Ùº\Ínm“H–oŒTN¹:.’$ùÐ›¸\ÅkSo¼®¼\é\ê™\î;Ã¶œ¥ü¹BÂ¡þ<Vh$\n±µ¥\Ú\Ú3(‘¤\ïˆl\"‘?øú´øÆ—_+~p\ä	32¿n\Þ5T×Ÿš\ö)e\Ê\Í$\ë¶z	\Ôý\n\á\'ù\ç\ãÔ±û\÷£\ñÖ¤\à\"\éµ\Û5S¼\Òþ¶¯\'¢•9\ôZ‹v\õ·9§\r€¼¸\Û\Ñ,\ë·‘\ô¶žS’\ÅÛ›ˆd<ž+5Uª\"I\ó)	\ås4I\ÕÇ“\Ù\Ô9n^ ’ 3§o\Ù\"Î¼!‘¼\ê1qü…â®HR¶E½‹úo°¯­‰Hª7p\Ýg¾CÇ±øT_#’ùJü\ñy¨H\ÖH¤xø<\ñØ¾ÿ!\Ý\óF\ñ\Øþ¿1#c°ë¦®—û	-Z\rúP}%\ãk_Àkc$Q—X¿ºcK¨žýC!µfù\Ü\\kRJd¨¾¨Rc\ëþ–Uµ¢l Ur„nMIO\Ì<\Ô\Ô\ÌK8c\ë…--­U‘,Pb¸F	•\ãº]o\ÝcDd\æ\ô-\â¤n?\"™z\ó\çømzl\ñ†\ê¼—}\õM43¢£:\Æ\âûÅš¹H\\¸\èT\Ä\'/ƒIúÅš:‰«²‘\Ï\Üÿ^\õ˜†]·€i\Z\ô©\\Oþzx¯ƒ¿Ž^¿\ÚcK ž\Ï=/\Ý:/%PJ¤\\“›­\ô\æÄŒ‹¤Ÿ\Ý -,\óX@rPnÅ—IO	l$’¡y%±˜±þ$’•©\n\")\Ü\Ø\ÍDdfb\ë¶\È\Ö\ö\ñ\âÂ»B[\Û<[x/´©7`Ÿ·\ñ¾zŽ\ð›r‰NÛ Ç”k\÷\Æø\"\Ü\Ö\Ì\ÇÀD’~­¦F\"\ÅC+_ú\ò1I\õº»™8¢iŸR–ª[\Û\ì\õà¯…ú{ˆ\ô«=¶„úqq\Ó\Ç\Õ5—”Ke,C\÷\ï+1‡#–\Þ|5\"@\ß%\Ï\Ã\ÉH2q úB®¸P\ð\ç:‹¨§`\õ±yc1›®³˜7\Åc2\Ø\ë•\Ïý¹ê¶¶9Áþ\ã»nˆ$h\Í\Èþ²\r½A¯)«\èg3\ó3(‘T?{X#‘\â\ëçˆ•›¤@\Ú\Ç$ž 9¢/‹2¥&}$l»:t³My½u†N\õ\ì¨¶\Âý\êŽ-To\â©\èZ3[oø\Æ\"³N\ó7FbYŒU\Í<fuú\æ\"\Ý^\'\0(·g\ËRÙ¢‰¤:”e\Æ9ž§¤\Î\Ä,\ZÊ±\Éy1\ãý)fY—vMOù\Zù\ØF\"\É\ç\æXP¾¦D´f”\"Qe¾ú|—VB0\àw\ö‰$ýZMDŠ¯¿_<r‰¤y\Ü”dk.&¼\0\00|@$AkFY$‡•A‰¤ú\Ù\Ã\Z‰_?[<r#‰¤y\Ü\0”¬¯)[¼€H\0Fˆ$h\rD2?É¯ü®ú¢qUv½V\ÝLC…>I\ÛØ”$y|ø\Æ\ßV+»þ»9h\Øvµ*\ãü™@ˆ$\0`t€H\öÅ²Xœ‹\Ë\æÐ²º$\ædý¬*‹²W„º~Ë‹¦M–\Ê$šÕ¥¹²\Ï\ìœXZ5\rD\"~j\Ü\ò¢­7%2wˆd~%’\0\0\0@N ’MQ’6\'\æ\æ|‘\\K¼ŽdpnI\Öú¤û)\ÑŽc\Ð\Z\Ø\ä\î˜Dü\Úqž\ö	D2?I\0\0\0£\0D²!Ë‹Z¶({ÇœLKš#€1K\ö[£\Ì)¹5™Ç¦\ë ø8\Õ/‘Em\0D2?I\0\0\0£\0D²O*\"I™?§\"Ð‡H\õ3¸Ä¶˜\çšX%\Ï:6]Á\ÇI…¤\íúrk»¡…H\æ\"	\0\0`€H\ö\É@D’Ú¤Ä•\Í$wuB\çe‹dM\öS­¥¿%D2?I\0\0\0£\0D²O&’Î¶t$F\É\àZ\ÖW¡Iˆd~ ’\0\0\0FˆdŸT\ä¬\égSý*m)‘Œˆ^\í:š\nbdý	 ’ùH\0\0 ’}R›\å\ã\ÙE’»b\Ë:\ÑÏ´Ÿ‹T\ã˜d\Æb8\Ô\ÇŽ[]5}\ìh\Éü@$\0\0Œ\É>	g\nù\r+,›\çH \é§poz)\Æ\ð$y¬O¥o,~jœ‰_\Ö\÷7D2?I\0\0\0£\0D´\"™ˆ$\0\0€Q\0\"	Z‘\ÌD\0\0À(\0‘­H\æ\"	\0\0`€H‚\Ö@$\ó‘\0\00\n@$Ak ’ùH\0\0 ’ 5\ÉüZ$Ïœ?\÷ª²<\ïUŸ³\÷™F\0Z@[\Ï;\ón}p\ã\çÜ¿3[_\áQ1{Ò´ø\ëÍ¡d¹û\ÉD\0À°\0‘­H\æg=D\ò\÷»š#\ó¦\r™m‘\âXÊŸ”\Ã3w±¯»[üµ”IþwG\ð\Ôp‘$\è\ï\Ò\ï\0. ’ 5\ÉüÔ‰ä£Ö¿¹>ù\ä“\Ñ~¾HÚŒÞ´ÁÚ¡¿¡\ô?F\Ô?XNbrI\âùªÏ‰E#™¾Hjù¤v\0À°‘­H\æ§N$\Ï:\ë,±k\×.sT…$’ú\ìÜ¹\ÓÔ¸ÔŠ\ä}»\Ä\ï›,‘Ú’\äoþ’\êø\ðV$\Õ1Ïºv\Ï\\\ÙRƒ¿~ž%“\ç\Éc¨vv~|Mª\Í;\'Z‡–-C©\í\Ø~\Ç\ösý¨”\×C\Ç\ãmþ5h\ò‰~^7úxKš˜H\ê5ø\ë\0I\Ð\Zˆd~\êDÒŠbH&m\Û%—\\bjª\ÄDÒ¾‘/w?Ç¤A·qIh\"’\ê8˜}\ÒÔµûT\æŒJ‰DŠ\ä,“%pI\Ö9kŸ;‰ULºü˜œ~\Æ\Ö]Ÿ\ÊZ‹s®J¡\ê[\ÄIcdL¯\õ\÷\Ï\Ë\'\ô:h\â\"©\æM\\S\0À\Æ‘­H\æ§\Ég$C2\ÙD\"	_\Ê\Ô|B|i\ó\Ç®¬ø,-+Z\êÚ«øsVD\'Iu>w½DhM•\Ý,¯\r­\ã¯\Ï\ô%–\ÖþIY\ï\Çti>¶\É\õ‹]«j›{®:Žûúùuu\óWQ\çi#\Ô\Z¢c‰\ó¡\ë\ßøu\0¬7\É\á))d\÷}\ãb\ß=‡\ÄMû\È\ò5q\óÁƒ\âÞ•\ñ])l	D2?Mo¶\á2\ÙT\"	zÓ§˜-!!£7þX|\Ñ\ÇÊŠ\ÏP;%u\í*kN›\Â\ÛÞ¦\ÂcWD2šqs¥J“–¿B´Œ\ì,V\äÔ¥\ñ\Ø\×/.eUQ\ì[$û~}¼s\ò \óNþC¥VŒSc5=\ô\n\n\Êˆ\äCv\×_W}\é+b\ç\â¢\Øù\ï‹\âŸ¯W…žSù\ì7‰ý\÷.‹gŸ}ÖŒZ_ ’ùi*’„\Èw½\ë]$’ 7vW$8úMÝ‘KO$ý\ñŽ¬$EGR\× 2g_1ª¢\ÒN$\Ý\ñ¡ºÇ¶¾~Z¹\0–\ëj&’ky}ø\õ\Õè¸©k¢Iˆ$2’\05\É!†\äkw\ïvq\é5W‹K¯¾Z\\þo\âŠ/\Þ ®ú\ò—e\Ù%þ\õ†\Åg®“\íŸŸ¾ú\Z\ñ…[\ö‰#R\Ú\Öˆd~úI‚dòª«®2G\õÐ›~T$U&Ï•%9ýˆ¤Š\ÏPÕ¶¨\Î\é\n^’À|é‹­É»…0\õ´\Ý^‰\é\Ñxll-–ºvO\Ì\Üu5\É\ÚøUBT—º%	‘$©m\0°@$‡˜[|M|\òŠÏŠOý\ëg\Å\ö\ÏÏ‹+o\Ú%®\Û\÷Uq\Ã\íwª\ò\ïK·‰\Ï}i·øÌµÿ¦úP\ß/\ÝúU3zý€H\æ§_‘\ì—Ð›~/\ê\Ø\ÍP†\Æû¥$‚	˜’\ö½‚u\í>•9SY³w1	\ng\ÅB\Ò\\“\']\Ô\Ç\nzNŸy4q\Z‹¤}ž\\K\êú\É\×\É\Þ`¤\ÚX¬¾ERR7_øú’Ñ¸H\Ò\Úý¿5\0À\ð\0‘¬°*–\æf\Å\ì,/sbi\Õ4–eýÜ’\ì\í±¼(f\Ùÿ\Õ\Òq0Ö²XÄµ<&el\Û?ÿ‹ø\ØgvˆKþ\õJ\ñ\Ù/\Þ(¾x\Û~q\ó¡eq\Û‰¯\Þÿuq\ó=ÿ!n\è\Ý)>w\ã—Ä§?w•˜\Ýù\Ï\âÿr…x¤Áw\æ\"™Ÿ\rI	½y[¢$$	}Š$Aýø\öª?¦®\ã\÷M~‘ß¢¯·.\"´^‚Ÿ;•Ðš\áQ2[®#\Ó\Ò\ï\Ø~®_Ë‹K¸±µ4\ò¸¼\ð9\ê\æw!d\óz¯/UaŒ‰$\ÕGþ±\0\0\n ’´Hr«KbNJ\à³¾\å\Å91\'û\ñ:I5.&‹i‘Üµt«øP\÷RqÆ¹\ç‰ÿ\Ñy»xûß¾S|~\Ï-\â\ö‡V\Ä\Ý\ßzL•ý|C\\/\å\ò\Ô3ÿ^üi\ç‰wŸs®ø\Çí—‹ß½\ÇDY ’ù´H‚„3-‹5øYÉ–´^\0`\àL”c2qŽAiª\Ù7/kWis‰\Æ;\ÂE²UŒ©\ö\×¶h²\ÔnŸk\Ôzœv6\ÞH_\õ4H\ÜØš+\ë¶\ès«ŒW™\År$’K«\ôE288o\Æ\åW]-¦?\ò1\ñ’c3ý˜8\÷¢±\åWS\\³{¯”\Èo‹»W¿-¾¸ÿ€8\ö\Ä×Š3\Î~Ÿ˜\í~Z¼üÕ“\â½ú°\èþ\ë•\ë*n\Éü@$ÁFC\Ü(‹™C&CZ\0À\ð1\á\n	VH\ê¸t\é~\\W—\æ’b˜U$•¨-J‰d*\ËWm£uU…SŸ_XD\Ë\ñ\ÅXO0\õúì‘Ž’\ó\Êyyl»|§ø\ë³\Þ\'~ú%/{ú™b[\÷2qüo½Vü\öÿ‰\è=ø°\Øÿ\õG\Ä\ÉùW\â“¿*>z\ñ\'\Å{\ßÿ\ñ\Â_~¥xû»\Þ-fwü\óº\ÞÁ\r‘\ÌD\0\0À(0QÊ‘²¥EoW\n\ÓË¬9’g\á’\Å\ÅN“O$m_š/T@‹/’4®‘të¹„\Ò\óB‘Ô¨v•\å×\âù×±d\Ç\ç®g^x‘ø±\ç¿P¼d\Ë\Ñ\â5¯{½x\ñ–ÿGü\ß/úu\Ã\ÍMw|M¼\à•G‹ü\ò/«¶_>\æ\Õ\âÇŸÿ\"\ñ·\ïŸ\Ý\Ï^i¢¬\Éü@$\0\0Œ¥q!³‚cž\ó-ZG-\\²lÕ ¨I+Z¼pQ\Ô\Ï)\ó©\ãø\"©\Ç8sTÐ¢\É\ç\ð|\ÏÀÏ…\ãŠ(I[D²€Úœ\öª\ì½\õ«bú?*Žû\í\×JA|¡øI)?ù\ó/ÿ\í/Ÿ¹vA|þË»\ÅOÿ\ÒKeý‹\ÅOQ½\ì\ó\ÒWOŠ?\ñ)q\ãÞ½&\Êú\0‘\ÌD\0\0À(P\ÍH\Ê\çV\Ø\nq\ã\"¹QI¾5o§\ñ\ô˜’IW‰Êº:N\Å•–\çíŠ¤Ä¶§DRR\á‰\'Ÿ\ç|›8ý\Ü\ó\ÄKŽ=^‰\ä\Ïÿ\Ê\ñ›¯{ƒ˜»nQü\ë¾(\Þp\òŸ‰¾\òUJ$_$\Ï8\÷|\ñ¡K>-}\ì1e}€H\æ\"	\0\0`\ð>#iDKIÛ¢XtŽ\Ý\"°\õøŒ\ä¢#`!‘´\Ïc¢\ÖB$•$ºu!!\Ô\×A\Êwx¶uŽ±µjn½}¿x\ï\ÌE\â}ÿ\ðb\ê\Ý\ï\ïøû³\ÅÇ·Ft¯¼J\\v\õ\çÅ§þ\å_Å»\Î9Wü\Õ\égŠ~lVœ\÷\ñ‹Å®¥%3:\0Ÿ3\ö|\r@$\ó‘\0\00\nxwm—¢E¢Td\ÖH4\n\ñ#´l\ÛÄ©¶TQ\ã\ÜyJl¸(Ê¾Ž\å\ÄD’ 6¿?a\êbcpB\ë\÷\Ö\'	g½µ\Z\å¥\ÓPÞ®ý\Â\Ä{Î»@ü\Ýù‰³.úxûßœ&Î•\ÂxÁ\'>¥\òœT|\à#—\åc\âs\×-¦o²‰\ÉcÃµÄ€H\æ\"	\0\0`Ø¸\ï‘t²’ 	\Ø\çþ\í\ß\Ä8Wœy\Þy\âÿ}û\Û\Õ\r6\Ïù/‹7½ù­R$?\"\Îù\ÐG\Ä\ó\óJ\Ú6ˆd~ ’\0\0\0Fˆ\ä@¶xÓ—Ô—“Ÿy\Þù\â\ï/¼H¼\÷¢\ñ¾øˆ\Ú\öžÿ\Â\r\ëúu?>\Éü@$\0\0Œøe›\â\à½\÷Š>þq\ñ\î|Pœq\Þ\òù6±ÿk_3­D2?I\0\0\0£\0DrÄ \Ì\ã=R\Ú-/o\ØV¶D2?I\0\0\0£\0D´\"™ŸA‹\ä\Ü\Î\â]§½#Y–\ö\Ýbz\0\0\0a ’ 5\ÉüZ$IŸ~ú\éhL\0\0hD´\"™ŸaÉ½{\÷@&\0\0$H‚\Ö@$\ó³\Ñ\"¹s\Çåª-\0\0\0@ˆ$h\rD2?¹E\ò\Äw\îGt}´¼\æ´=A¡¤\ÉCbfrBLL\Ø\Ò\ó¦e4˜‰I1s\È\Ä\êØ„\ôºbjª+z\æP¡\ê¦T™^X1•‰>½®®Ÿšš¡\áe»763\Öeaº¨¯œ\'tŽczA–\ß\äúŒ+bZ^ˆ$h\rD2?¹E2$~	I$• Hšf[\ó)““3R/Gˆ$gV\ÄÂ´”¡nWt¹$)1°\Ç=\Ù’Aª\÷!\éKÊ•Œ¿P\Z‰\í¯\ç\êm!\"\çX@\ñd{D$\Ã\ñ#\ëW\è\ïE^$ˆ$h\rD2?ƒÉ‹¯}@\ì¼\éa\ñ¦³oUu\ôH\ÇToE\ò„\í«N‰Š¤\Ï|\"	À\ÈÁÅˆ¼`º’\õ«ˆ!e\ä˜a•}d¬ˆ”…!\Ñ3\"\Éaý%½nS‰s\Ï\ÑBst¤EE2¿\Ñ:\Çy=\èü!’ 5\ÉüB$\ßr\á\í\âŽûŸ\ï¹\ô ª;ÿŠe±ûÀcª¾ïŒ¤e$\'ý¥\Ý\ö\î\ðMo5\ÛV\n[¸¿/uü\Øm;43\éÄ£Œ\éd1Oh\Û=&Œ^}0\õ±u²pŽ\ö—1\ç\Ë6~­\Ü1¢¼\\‰y\0\ÈBÿ\"Y©³r¥)û§·}c™¾’r\îhL¾V“m4sùkt	ˆ¤É¤©G»Nš³Xs8~³uŽ6k‘­H\æg\"yÌ©»\Ô\ók\÷V…$’ z+’/;c¿S’\"\É\È#_\Ø\ä±\"¿\Þ\Â\ëcƒm\òù\ä¤\\Kd\Ü|\'°>\ê\Ã$\Í)uq¼¹}a\ö—q­ª\ë\Æ\Ç3y¬´…\æ žd‘y²\æKZR$û\Ø\æ\æ\íM-\Î!•\ôE’e6£\"\É)\ãC$9\åu„H‚\Ö@$\ó3¨\ÏH>xXÇµ\Û\Ûtl\Ûx’—&Id¢C[\Ý13\õÊšª\Ò9[j\Ó\Ï)›Ù™g\ñ¼Ÿ*NV”\ð\æ/h\Ç]—+¬/•Ð¹J\ôš\å5\ÆÄ¢-6\0Ù¨f\ëH–t&nZt»ž8I’\"É¥**YUAMZXh9iiu\ÏÑ™‹‹d\"\É`\×\"	Z‘\ÌÏ D’2‘?y¤J:\æ\"iŸ\óºFŸ‘¬˜•#º»»”(W’\êúûÆ\Ís\Ú.\öe- gUüØ–&qøX¶\ÞFý	}\Ç{3‘\Ì@6ª\"\É!ªx’\'O…\\5I–\r\ä\Äb\Æú{\×YÀÏ‘ž—[\ÖE©‘\É\"~t\ã?wˆ$h\rD2?ƒ\ÉT\áYH^B\"yh¦\ãJ\Ê(\Z!¢\ç\Ñm\\+ML’’ý¹<\ñczN™ºP_\Ý\ßn\'üØ–&qx&…\Éþ¬Þ‘GÝ¦\ÇK*m¡y\0\ÈEB$Iš\nÁ¢~l;\Ø3+zü¹\Î\"j\çb\õA¹”\Äb\Æús\ÔX;oŠ9Gž‘tÎ—Á\ãG\Ï}\Üp¯)D´\"™Ÿ\Ü\"™ý{$­h*<«¦¥G\ÕOv\Ô\çgiar\ÇP¡q¡þ‡‹Áu¼RÚ¼¾J\È\Ø<\óc[š\Ä\ÑscGûOŠN‡¶ÿu½³gŒ¾¶^–\Ê9\0\Ð_²\è\Øf\êüz&M$]¦Ÿ\ãyJ´\Ìø¢¡KY,;Î–\"£ˆ\ï\Ï×™\ÊFþ92¢\"™ˆ;\÷1\Â\Ï\êB$Ak ’ù\É-’>$‡!i•f[\Ûuq\Ù$Bu›-’Ui\0€\Ñ\Ã\Ï\ÄB$Ak ’ùHn& ’\0€\ÍDd\"™ŸA‹\ä\Ü\ÎJ›\ê\Ú\0‘\0l^ ’ 5\ÉüZ$\0\0€@$Ak®ƒHf\"	\0\0`€H‚\Ö #™ˆ$\0\0€Q\0\"	Z‘\ÌD\0\0À(\0‘­H\æ\"	\0\0`€H‚\Ö@$\ó3h‘lr\×\öÒ¾[Lo\0\0\0 D´7\Û\äg\Ð\"I¢ú\ÎH[ “\0\0\0š\0‘­AF2?\Ã ’{\÷\îL\0\0H‘­H\æg£Er\çŽ\ËU[\0\0\0€É¦¬.‰¹\ÙY1«Ê¢X6\Õ.\ËbQ¶\Ï-­šcºË‹¦M–\Å\ð«KseŸ\Ù9\áL•ˆŸ\Z·¼h\ëM‰\Ì\"™Ÿ\Ü\"y\â;\÷Š£Nº>Z^sÚž PR‰‰\ä|gBLL\è2™øÙ–C3“E?§túùqÄ–¿shFL®uü|§X³sž±ú‘¾M¯¡\"#|m\Ç\ág\'Az]15\Õ=s¨PuSªL\ó\ßÁ\ã$ú\ôºº~\Êû=K\ÙîÄŒ\õ_Y˜.\ê+\çÀ	£AÅ˜^e\Æ\ã7¹>\ã\ÂÊ‚˜–\×\"ÙˆU±47+\n¿\"\á›[’µ.$dsss‘L\ÇP¢ˆ\é@¢\È$\Ï“ˆ_;\Î\Ò>H\æ\'·H†\ä\Ñ/!‰¤I)f3…­\ô)yJˆú•ú™Aš×®•­A‰i >H<F\ók‰\áAbY+¤\0HuZ˜–2\Ô\íŠ.—$%\ö¸WùMe\rÕ‡û\ô%\åJ\Æ_(ŒÄŒ\ö\×su‹¶‘s, x²=\"’\áø‘uŽ+\ô\÷\"/D²	$bŽ\ä\ä‹\ÄM\Ê\ZIZP$“1\Ö(s*i2M\Öh\á\ãT¿X†µ\ÉüB$/¾\ö±\ó¦‡Å›Î¾U\Õ\Ñ#S½\É¶¯:%*’‡\Ä\ÌdJ‚8$A¢¯d¤¢N´I/[¬5_Ø’‰\áRs\r\Å\à²	@¸‘LW²~1¤Œ3¬²Œ‘²0$zFÄ¢19¬¿¤\×m*q\î9ZhŽ\î‚¡¨H\â7Z\ç!¯?D²	F9”},«hK[\ËXT$S1Œ.±-\æ\è\ö8‡gk\×\È\à\ã\Ô\ÚÙ¶¶¿]\Þ\0ˆd~!’o¹\ðvq\ÇýOˆ\÷\\zPÕÅ²\Ø}\à1U\ßwFÒ¡¹À\0ù[\Ú|{\×iSY?]?93\ãˆdxŒ‘Í™\êp\ÑfY\ìTv´\"lF\èüú°\Øib1\\\Ò×°QY[\0aú\ÉJ•+\õH\Ù?½\í\Ë\ô•”sGc:\ðµšl£™\Ë_£K@$M&M=\ÚuÒœÅš\Ã\ñ›­s|°Y[ˆdj$?_“HR›”¸²™\ä®Nè¼Œcc‘¬\É~ªµ\ô—¡„H\æg\"yÌ©»\Ô\ók\÷V…$’ z+’/;c¿Sšˆ$I]#Q\ò–\Ê*rÙ£\çe\æ’Dj\"8¶:¦,’­\àv0N‡q‹\nœ›²‰\ñk\ÐD\ë®a}Œ~²\Â\0X<\É\"1\òdÍ—´¤H\ö±\Í\ÍÛ›Z<C*;\é‹$\ËlFE’SÆ‡Hr\Ê\ë‘lB²¶5‹¤³-\ÍÚ‚z\í©øqš\ôqH\ægPŸ‘|\ð°Žk··\éØ¶\ñ,$/q‘L”K¢¯’2›42D\Ò99#GYª\òW\ã\÷‰É£“4\Å;KJ\à´\Ü\êù;¯#-Í®a­H\Ò9E\Î€8\ÕlÉ’\Î\ÄM‹n\×\'IR$¹TE%«*¨iA-\'-­\î9:sq‘L`\ãC$\ì\ÚA$›ýü¡–®r[˜O\ã1\è©ß–Éˆ\è¥\â+\"\ã*ø\ã\êH\ægP\"I™\ÈÇŸ<RH%s‘´\Ïy]X$ûË€)\ér\ÄÐ ¤Žg\ö˜\ì\ÅD26\ÆG\"%’\ñmdO\Ø*Bg Œb\Ô\ã¢1ú¸†5\ë cx$èŸªHrH *ž\ä\ÉS!WD’e9±˜±þÁu\ðs¤\ç\å–uQjd²ˆ]\çøÁ\Ï\"\ÙO\ÂD‹“‘$¹“R©Ç¥b\è6w“\ÌX‡úøÁqR†Í¬šÄ¹Å€H\ægP\"™*<\ÉKP$ýŒX_\ð\Ç\n£<.~‘­\í\ä>OD$M\ìº, Â‘N?¾¯\'D,F?\×0¹Žþ¤€’„H’4‚Eý\Øv°#fV\ôøsE\Ô\Î\Å\êƒr)‰ÅŒ\õç¨±v\Þ/rŽ<#\éœ/ƒÇžû¸\á^SˆdcøM)\ñŒ]\\$‰T\÷¦—bA’\ÇúTú\Æ\â§Æ™øe}ÿwpC$\ó“[$s¤;w{8&fÎ1¼(‰\"	2Ç“\Ñ\áBD¢eúº7\Û\Ä\Æø‚Å½6%f&•”Ð±u”\Ý(ž\ß »ˆ\Ñ\Ï5T\×A\ÐZ\ZfXp\ð%‹Žm¦Î¯g\ÒD\Òeú9ž§DËŒ/\ZÊ±”Å²\ãl)2z˜\ñþ|©l$\áŸ##*’‰ø±s#ü¬.D´\"™Ÿ\Ü\"\éCr’\ÆP‰F\0\0À¸\ágb!’ 5\ÉüŒ¦H\ò,-£’)Ë±\öa‰\0\0ƒ\"	²‘\ÌÏ Ern\ç%ˆM\n\õ\0\0\0B@$Ak ’ù´H\0\0\09€H‚\Ö@$\ó‘\0\00\n@$Ak ’ùH\0\0 ’ 5\Éü@$\0\0ŒI\Ð\Zˆd~ ’\0\0\0†!þ\ï\è1\Õ\õ\\\0\0\0\0IEND®B`‚','2025-06-30 07:48:27'),(4,2,'1232132132132321',NULL,'2025-06-30 07:48:48'),(5,2,'ÐŸÑ€Ð¸Ð²ÐµÑ‚!!!',_binary '‰PNG\r\n\Z\n\0\0\0\rIHDR\0\0,\0\0z\0\0\0:Hž\0\0KiCCPICC Profile\0\0H‰•WXS\Éž[R!D@J\èM‘@J-€\ô\"ˆJH„cBP±£‹\n®]D°¢« Š±aW\Å\îZ*+\ëbÁ®¼	t\ÙW¾7\ß7wþûÏ™\Î9w\æ\Þ;\0\Ð\ÛùRiª	@®$O\ì\Ï\Z—”\Ì\"uP\Z ¾@.\åDE…XÚ¿—w7¢l¯9(µþ\Ùÿ_‹–P$\0€DAœ&”r!>\0\Þ$\Ê\ò\0 J!o>5OªÄ«!Ö‘A!®R\ânR\â4¾\ÒgÃ…ø	\0du>_–€F7\äYù‚¨C‡\Ñ\'‰P,\ØbŸ\Ü\Ü\ÉBˆ\çBlm\àœt¥>;\íŒ¿i¦\rj\òùƒXK_!ˆ\å\Òþ\ôÿ3ÿ»\ä\æ(æ°†U=S£Œ\æ\íI\ö\ä0%V‡øƒ$-\"bm\0P\\,\ì³Wbf¦\"$^e\Ú\ä\\˜3À„xŒ<\'–\×\Ï\ÇùaBœ.É‰\ï·)L)m`þ\Ð2q/b=ˆ«D\òÀ\Ø~›²\É1\ó\ÞL—q9ýüs¾¬\Ï¥þ7Ev<G¥igŠxýú˜cAf\\\"\ÄTˆ\ò\Å	k@!ÏŽ\r\ë·I)\È\äF\Ø\È1\ÊX, –‰$Áþ*}¬4]\Óo¿3W>;v\"SÌ‹\è\ÇW\ó2\ãBT¹Âžø}þ\ÃX°n‘„? #’ˆE(\nTÅŽ“E’øX\ëI\óücTcq;iNT¿=\î/\Ê	V\òf\Ç\É\óc\Æ\æ\çÁÅ©\ÒÇ‹¤yQq*?\ñ\ò,~h”\Ê|/\\\0X@k\Z˜²€¸µ«¾Þ©z‚\0\È@‡~f`Db_^cAø\"Ž\ó\ï\ë|\È\Â*9\ñ §º:€\ôþ>¥J6x\nq.9\ð^Ñ§$\ô <Œø\ñaÀr`U\öÿ{~€ý\Îp \Þ\Ï(fd\Ñ,‰\Ä\0b1ˆh‹\à>¸¯~°:\ãl\Üc Ž\ï\ö„§„6\Â#\Â\rB;\á\Î$q¡lˆ—cA;\Ô\ê\ÏOÚùÁ­ ¦+\î{Cu¨Œ3q\à€»Ày8¸/œ\Ù²\Ü~¿•Ya\r\Ñþ[?<¡~;Š¥£øQl†ŽÔ°\ÓpTQ\æú\Çü¨|M\Ì7w°g\èü\Ü²/„m\ØPKlv\0;‡\Ä.`MX=`aÇ±¬;ªÄƒ+\îIßŠ˜-¦ÏŸl¨3t\Í|²\ÊLÊjœ:¾¨ú\òD\Óò”›‘;Y:]&\Î\È\Ìcq\àC\Ä\âIŽ#X\ÎNÎ®\0(¿?ª\×Û›\è¾\ï\n\Âlù\Î\Íÿ\0\ïã½½½G¾s¡\Ç\Ø\ç_	‡¿s6løiQ\àüaB–¯\âp\å…\0\ßt¸û\ô1060g\à¼€¡ Ä$0zŸ	×¹L3Á<PJÀr°”ƒM`+¨»Á~PšÀIp\\WÀ\rp®ž\ðtƒw\à3‚ $„†0}\Ä±D\ìg„ø H8ƒ$!©H\"A\ÈLd>R‚¬DÊ‘-H5²9ŒœD. m\È\ä!Ò‰¼F>¡ªŽ\ê F¨:e£4C\' \è´\0]€.E\Ë\ÐJtZ‡žD/¡7\Ðv\ôÚƒL\rcb¦˜\ÆÆ¸X$–Œ¥c2l6VŒ•b•X-\ÖŸ\ó5¬\ë\Â>\âDœ³p¸‚C\ðx\\€OÁg\ãK\ðr¼\n¯\ÃO\ã\×\ð‡x7þ@#\ì	ža!ƒ0•PD(%l\'\"œ{©ƒ\ðŽH$2‰\ÖDw¸“ˆY\Ä\Ä%\Ä\r\Ä=\Ä\Ä6\âcb‰D\Ò\'Ù“¼I‘$>)TDZG\ÚE:NºJ\ê } «‘M\È\Î\ä r2YB.$—’w’‘¯’Ÿ‘?S4)–OJ$EH™NYF\ÙFi¤\\¦tP>Sµ¨\ÖToj5‹:ZF­¥ž¡Þ£¾QSS3S\óP‹V«\ÍU+SÛ«v^\í¡\ÚGumu;u®zŠºB}©ú\õ\êw\Ô\ß\Ðh4+š-™–G[J«¦¢= }\Ð`h8j\ð4„\Zs4*4\ê4®j¼¤S\è–t}\"½€^J?@¿L\ïÒ¤hZir5ùš³5+4k\Þ\Ò\ì\ÑbhÒŠ\Ô\Ê\ÕZ¢µS\ë‚\Ösm’¶•v ¶P{\öV\íSÚÃœÁe\ó\Ûg:DkžN–N‰\ÎnVn]m]\Ý\ÝiººGuÛ™ÓŠ\Éc\æ0—1\÷3o2?\r3\Z\Æ&\Z¶xX\í°«\Ã\Þ\ë\r\×\ó\Ó\é\ë\íÑ»¡\÷IŸ¥¨Ÿ­¿B¿^ÿ¾n`gm0\Õ`£Áƒ®\á:Ã½††\ß?ü7C\Ô\Ð\Î0\Æp†\áV\Ã\Ã#c£`#©\Ñ:£SF]\ÆLc?\ã,\ã\Õ\ÆÇŒ;M&>&b“\Õ&\ÇMþ`\é²8¬V\ë4«\Û\Ô\Ð4\ÄTaºÅ´\Õ\ô³™µY¼Y¡\Ù³û\æTs¶yºùj\óf\ón‹±3-j,~³¤X²-3-\×Zž³|oem•hµÐª\Þê¹µž5ÏºÀº\Æúž\r\Í\Æ\×fŠM¥\Íu[¢-\Û6\Ûvƒ\í;\Ô\Î\Õ.Ó®\Â\î²=j\ïf/¶\ß`\ß6‚0\Âc„dD\åˆ[\ê‡|‡\Z‡‡ŽL\Çp\ÇB\ÇzÇ—#-F&\\1\ò\Ü\ÈoN®N9NÛœ\îŽ\Ò:ªpT\ã¨\×\Îv\Î\ç\n\ç\ë£i£ƒF\Ï\Ý0ú•‹½‹\Èe£\ËmW†\ëX×…®Í®_\Ý\Ü\Ýdnµn\î\î©\î\ë\Ýo±u\ØQ\ì%\ì\ó9M=\Ý<\ó<\÷{þ\å\å\à•\íµ\Ó\ëù\ë1¢1\Û\Æ<\ö6\ó\æ{o\ñn\÷aù¤úl\öi\÷5\õ\åûVú>\ò3\÷úm\÷{Æ±\ådqvq^ú;ù\Ëüù¿\çzrgqO`Á\Å­Ú\ñ\å‚Ì‚2‚j‚ºƒ]ƒgŸ!„„…¬¹\Å3\â	xÕ¼\îP\÷\ÐY¡§\Ã\Ô\Ãb\Ã\Ê\Ã…Û…\Ë\ÂÇ¢cCÇ®\Z{/\Â2BQ	\"y‘«\"\ïGYGM‰:MŒŽŠ®ˆ~\Z3*ffÌ¹XF\ì¤Ø±\ï\âü\ã–\ÅÝ·‰W\Ä7\'\ÐRª\Þ\'$®Ll7rÜ¬q—’’\ÄI\rÉ¤\ä„\ä\í\É=\ãÇ¯ß‘\âšR”rs‚\õ„i.L4˜˜3\ñ\è$ú$þ¤©„\Ô\ÄÔ©_ø‘üJ~O\Z/m}Z·€+X+x!\ô®vŠ¼E+E\ÏÒ½\ÓW¦?\Ï\ð\ÎX•Ñ™\é›Yš\Ù%\æŠ\ËÅ¯²B²6e½ÏŽ\ÌÞ‘Ý›“˜³\'—œ›š{X¢-É–œžl<y\Ú\ä6©½´H\Ú>\ÅsÊš)Ý²0\Ùv9\"Ÿ o\ÈÓ?ú-\n\ÅOŠ‡ù>ùù¦&L=0MkšdZ\Ët»é‹§?+*øe>C0£y¦\é\Ìy3\Î\â\Ì\Ú2™6»yŽùœs:\æÏ­šG—=\ï\×B§Â•…o\ç\'\Îo\\`´`\î‚\Ç?ÿTS¤Q$+ºµ\Ðk\á¦Eø\"\ñ¢\ÖÅ£¯[ü­XX|±Ä©¤´\ä\ËÁ’‹?ú¹\ì\çÞ¥\éK[—¹-Û¸œ¸\\²ü\æ\n\ßU+µV¬|¼jìªºÕ¬\ÕÅ«ß®™´\æB©Ké¦µÔµŠµ\íe\áe\r\ë,\Ö-_\÷¥<³üF…Åž\õ†\ë¯¿A¸\á\êF¿µ›Œ6•lú´Y¼ù\ö–\à-u•V•¥[‰[\ó·>Ý–°\í\Ü/\ì_ª·l/\Ùþu‡dG{UL\Õ\éj\÷\êê†;—Õ 5Šš\Î])»®\ì\Ø\ÝP\ëP»esO\É^°W±\÷}©ûn\î\Û\ß|€} \ö \åÁ\õ‡‡Šëº\éu\Ý\õ™\õ\í\rI\rm‡C77z5:\âxdG“iS\ÅQÝ£ËŽQ-8\Ö{¼\àx\Ï	é‰®“\'7Oj¾{jÜ©ë§£O·ž	;sþl\Ð\ÙS\ç8çŽŸ\÷>\ßtÁ\ó\Â\á‹\ì‹\õ—\Ü.Õµ¸¶ú\Õ\õ\×C­n­u—\Ý/7\\\ñ¸\Ò\Ø6¦\í\ØUß«\'¯\\;{wýÒˆm7\ãoÞ¾•r«ý¶\ð\ö\ó;9w^ý–ÿ\Û\ç»s\ï\î\ß×¼_úÀ\ðA\åï¶¿\ïiwk?ú0\àaË£\ØGw¿x\"\ò¥cÁS\Ú\Ó\Òg&ÏªŸ;?o\ê\ê¼\ò\Çø?:^H_|\î*úS\ë\Ï\õ/m^ü\Ëï¯–\îq\Ý¯d¯z_/y£ÿf\Ç[—·\Í=Q=\Þ\å¾ûü¾øƒþ‡ª\ì\ç>%~z\öy\êÒ—²¯¶_¿…}»×›\Û\Û+\å\Ëø}¿Pm\Òx½\0Z\0xn¤ŽWû\n¢:\Ó\ö!\ðŸ°\ê\ÙW\Ü\0¨…ÿ\ô\Ñ]\ð\ï\æ\0{·`\õ\é)\0D\Ñ\0ˆ\ó\0\è\èÑƒu\à,\×w\îT\"<lŽøš–›þMQI\ð{h”ª.`hû/1ƒ\n\é·IS\0\0\0ŠeXIfMM\0*\0\0\0\0\Z\0\0\0\0\0\0\0>\0\0\0\0\0\0\0F(\0\0\0\0\0\0\0‡i\0\0\0\0\0\0\0N\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0’†\0\0\0\0\0\0\0x \0\0\0\0\0\0, \0\0\0\0\0\0z\0\0\0\0ASCII\0\0\0Screenshot›‚k\ä\0\0\0	pHYs\0\0%\0\0%IR$\ð\0\0\ÖiTXtXML:com.adobe.xmp\0\0\0\0\0<x:xmpmeta xmlns:x=\"adobe:ns:meta/\" x:xmptk=\"XMP Core 6.0.0\">\n   <rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">\n      <rdf:Description rdf:about=\"\"\n            xmlns:exif=\"http://ns.adobe.com/exif/1.0/\">\n         <exif:PixelYDimension>378</exif:PixelYDimension>\n         <exif:PixelXDimension>556</exif:PixelXDimension>\n         <exif:UserComment>Screenshot</exif:UserComment>\n      </rdf:Description>\n   </rdf:RDF>\n</x:xmpmeta>\nBv‰\0\0\0iDOT\0\0\0\0\0\0\0\0\0\0½\0\0\0(\0\0\0½\0\0\0½\0\0	$pÀŸ\0\0\ðIDATx\ì\Ö1\00±†?\è¦W?(r²\Ï}w @ ,0K8¯ @€\0_À`Q @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0y\0\0ÿÿª\Ö!¦\0\0\îIDAT\í\Ö1\00±†?\è¦W?(r²\Ï}w @ ,0K8¯ @€\0_À`Q @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yƒ%‘	 @€\0ƒE @€\0¼€Á’Èƒ @€€Á¢ @€@^À`\ÉG\äA @À`\Ñ @ /`°\ä#\ò  `°\è\0 0X\òy\00Xt€\0\È,ùˆ<H€\0,:@€\0\ä–|D$@€\0 @€\0\òK>\" @€\0‹ @€\0yCB\ã\ÞÞºª\0\0\0\0IEND®B`‚','2025-07-01 05:33:20');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quiz_id` int NOT NULL,
  `text` text NOT NULL,
  `question_type` varchar(20) NOT NULL,
  `options` json DEFAULT NULL,
  `correct_answer` json DEFAULT NULL,
  `order` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_id` (`quiz_id`),
  KEY `ix_questions_id` (`id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quizzes`
--

DROP TABLE IF EXISTS `quizzes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quizzes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `is_test` tinyint(1) DEFAULT NULL,
  `department_id` int DEFAULT NULL,
  `access_level` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `department_id` (`department_id`),
  KEY `access_level` (`access_level`),
  KEY `ix_quizzes_id` (`id`),
  CONSTRAINT `quizzes_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`),
  CONSTRAINT `quizzes_ibfk_2` FOREIGN KEY (`access_level`) REFERENCES `access` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quizzes`
--

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;
/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL,
  `role_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'ÐÐ´Ð¼Ð¸Ð½'),(2,'ÐŸÐ¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»ÑŒ');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES (1,'ÐÐ´Ð¼Ð¸Ð½Ð¸ÑÑ‚Ñ€Ð°Ñ‚Ð¸Ð²Ð½Ð°Ñ Ð´Ð¾ÐºÑƒÐ¼ÐµÐ½Ñ‚Ð°Ñ†Ð¸Ñ'),(2,'ÐžÐ±ÑƒÑ‡ÐµÐ½Ð¸Ðµ'),(4,'ÐŸÐ¾Ð´Ð´ÐµÑ€Ð¶ÐºÐ°'),(5,'ÐœÐ°Ñ€ÐºÐµÑ‚Ð¸Ð½Ð³Ð¾Ð²Ñ‹Ðµ Ð¼Ð°Ñ‚ÐµÑ€Ð¸Ð°Ð»Ñ‹');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int NOT NULL,
  `department_id` int NOT NULL,
  `access_id` int NOT NULL,
  `auth_key` varchar(255) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_UNIQUE` (`login`),
  KEY `role_id_idx` (`role_id`),
  KEY `fk_user_department_idx` (`department_id`),
  KEY `fk_user_access_idx` (`access_id`),
  CONSTRAINT `fk_user_access` FOREIGN KEY (`access_id`) REFERENCES `access` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_department` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Ð¢Ð°Ð±Ð»Ð¸Ñ†Ð° Ð´Ð»Ñ Ð¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»Ñ';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'Pavel2','$2b$12$vh49FcYIBzIVD8GqMBpOzOOxOGpJG37ytdLH/MbBfn/QmEvd4B8pu',1,5,3,'4fde95cb171b803e85465ce491ad1b23','Ð ÐŸ Ð','2025-06-25 09:30:15','2025-07-01 05:58:31'),(6,'Pavel3','$2b$12$vh49FcYIBzIVD8GqMBpOzOOxOGpJG37ytdLH/MbBfn/QmEvd4B8pu',2,1,2,'1699617cda29608f8c814bbd2ce8582f','Ð ÐŸ Ð','2025-06-25 09:30:15','2025-06-25 09:31:10'),(8,'jopa','$2b$12$pZNdNf4FN3moLk.MxX0oaOKSvFu94lzTdcn2XQwKyHj8uToW6I4hK',2,5,3,NULL,'Ð ÐŸ Ð','2025-06-25 09:30:15','2025-06-25 09:31:10'),(9,'Pavel4','$2b$12$tcbVuXDwxTJIoltdQIRxKeyt9sxrryKPtFdSyPfLe2ScZRYXGznLy',1,5,3,'e8323a063c0af5c8d4829eaedae459ba','ÐÐµÐ²ÐµÑ€Ð¾Ð² ÐŸÐ°Ð²ÐµÐ» ÐÐ½Ð´Ñ€ÐµÐµÐ²Ð¸Ñ‡','2025-06-25 09:30:15','2025-06-25 09:39:11'),(10,'jfgfg','$2b$12$IkM6.lrIqdHzLi6WLQsUie1txrnHfG0FD16d1xftODi8O.a/pfnwC',1,5,3,NULL,'ÐÐµÐ²ÐµÑ€Ð¾Ð² ÐŸÐ°Ð²ÐµÐ» ÐÐ½Ð´Ñ€ÐµÐµÐ²Ð¸Ñ‡','2025-06-25 09:30:15','2025-06-25 09:39:00');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_answers`
--

DROP TABLE IF EXISTS `user_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `attempt_id` int NOT NULL,
  `question_id` int NOT NULL,
  `answer` json NOT NULL,
  `is_correct` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  KEY `ix_user_answers_id` (`id`),
  KEY `user_answers_ibfk_1` (`attempt_id`),
  CONSTRAINT `user_answers_ibfk_1` FOREIGN KEY (`attempt_id`) REFERENCES `user_quiz_attempts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_answers_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_answers`
--

LOCK TABLES `user_answers` WRITE;
/*!40000 ALTER TABLE `user_answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_quiz_attempts`
--

DROP TABLE IF EXISTS `user_quiz_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_quiz_attempts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `quiz_id` int NOT NULL,
  `started_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `score` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_user_quiz_attempts_id` (`id`),
  KEY `user_quiz_attempts_ibfk_1` (`user_id`),
  KEY `user_quiz_attempts_ibfk_2` (`quiz_id`),
  CONSTRAINT `user_quiz_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_quiz_attempts_ibfk_2` FOREIGN KEY (`quiz_id`) REFERENCES `quizzes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_quiz_attempts`
--

LOCK TABLES `user_quiz_attempts` WRITE;
/*!40000 ALTER TABLE `user_quiz_attempts` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_quiz_attempts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-02 14:54:59
