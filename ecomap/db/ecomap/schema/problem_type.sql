/*
    This table provides names of all
    problem types.
*/
CREATE TABLE IF NOT EXISTS `problem_type` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `type` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
