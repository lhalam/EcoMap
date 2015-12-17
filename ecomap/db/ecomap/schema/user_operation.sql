/*
    This table stands for holding gererated
    hashes for password restoring. 
*/
CREATE TABLE IF NOT EXISTS `user_operation` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hash_sum` varchar(255) NOT NULL,
  `creation_date` int(11) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `activity_type` int(11) unsigned NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
