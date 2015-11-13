/*
    This table holds all particular
    information about problem entity.
*/
CREATE TABLE IF NOT EXISTS `problem` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
 `title` varchar(255) NOT NULL,
 `content` varchar(255) NOT NULL,
 `proposal` varchar(255) NOT NULL,        # User can propose a solution
 `severity` enum('1', '2', '3', '4', '5') NOT NULL DEFAULT '1',
 `status` enum('Solved', 'Unsolved')
        NOT NULL DEFAULT 'Unsolved',    # not resolved or resolved
 `latitude` float NOT NULL,           # coordinats of
 `longtitude` float NOT NULL,         # location
 `created_date` int(11) unsigned NOT NULL, # date of creation
 `problem_type_id` int(10) unsigned NOT NULL,
 `user_id` int(10) unsigned NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
