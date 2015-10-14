/*
    This table provides description of all problem types
*/
CREATE TABLE IF NOT EXISTS `problem_type` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `type` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
