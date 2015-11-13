/*
    This table represents logging of all
    activities produced on exact problems.
*/
CREATE TABLE IF NOT EXISTS `problem_activity` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `created_date` int(11) unsigned NOT NULL,     # Time of activity's occuring
    `problem_id` int(10) unsigned NOT NULL,
    `user_id` int(10) unsigned NOT NULL,
    `activity_type` enum('Added', 'Removed', 'Updated', 'Vote') NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
