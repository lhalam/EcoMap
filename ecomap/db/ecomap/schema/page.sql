/*
    This table holds static info - pages.
    Pages are instructions or F.A.Q. of
    solving some ecological problems.
    Only administators can modify and create
    pages.
*/
CREATE TABLE IF NOT EXISTS `page` (
  `id` int(10) unsigned NOT NULl AUTO_INCREMENT,
  `alias` varchar(100) NOT NUll,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `content` text NOT NULL,
  `meta_keywords` varchar(255) NULL,
  `meta_desription` varchar(255) NULL,
  `is_enabled` boolean NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
