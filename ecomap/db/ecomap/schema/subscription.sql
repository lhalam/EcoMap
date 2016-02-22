/*
    This table connects a problem
    and a user, who has voted for this
    particular problem.
*/
CREATE TABLE IF NOT EXISTS `subscription` (
  `id` int(10) unsigned NOT NULl AUTO_INCREMENT,
  `problem_id` int(10) unsigned NOT NUll, # problem, wich was voted
  `user_id` int(10) unsigned NOT NULL ,   # user who has voted
  `date_subscriptions` int(11) YES NULL ,
  `severity` enum('1', '2', '3', '4', '5') NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
