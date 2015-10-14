CREATE TABLE IF NOT EXISTS `page` (
  `id` int(10) unsigned NOT NULl AUTO_INCREMENT,
  `alias` varchar(100) NOT NUll,
  `title` varchar(100) NOT NULL,
  `description` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `meta_keywords` varchar(255) NULL,
  `meta_desription` varchar(255) NULL,
  `is_enabled` boolean NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
