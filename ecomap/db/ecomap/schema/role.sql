 /*
    This table contains all role names
    and their ids.
 */
CREATE TABLE IF NOT EXISTS `role` (
  `id` int(10) unsigned NOT NULL  AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  UNIQUE (name),            # name of role
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
