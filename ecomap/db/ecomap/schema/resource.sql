CREATE TABLE IF NOT EXISTS `resource` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `resource_name` varchar(100) NOT NULL,    # name of resource
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
