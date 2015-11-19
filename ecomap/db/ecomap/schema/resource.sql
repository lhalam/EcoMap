/*
    This table contains name of the
    resource and it's id. Resources are
    any action or data. This table is
    needed for rights restriction.
*/
CREATE TABLE IF NOT EXISTS `resource` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `resource_name` varchar(100) NOT NULL, # name of resource
  UNIQUE (`resource_name`),
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;