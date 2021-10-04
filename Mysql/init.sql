CREATE database IF NOT EXISTS dev;
USE dev;
CREATE TABLE IF NOT EXISTS `predictions`(
 `id` int(11) NOT NULL auto_increment,
-- `prediction_type` int(11) NULL,
 `prediction` varchar(20) NOT NULL default '',
 `img` varchar(40) NOT NULL default'',
 PRIMARY KEY (`id`)
);