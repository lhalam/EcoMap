/*
    This table created for gathering information about
    user for transfering to another tables.
*/
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `avatar` varchar(255),
  `password` varchar(100) NOT NULL,
  `oauth_provider` varchar(100),    # this atttribute will specify provider name
  `oauth_uid` text,                 # this attribute will specify open auth id
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
