/*
    This table connects a problem
    and a user, who has voted for this
    particular problem.
*/
CREATE TABLE IF NOT EXISTS `subsription` (
  `id` int(10) unsigned NOT NULl AUTO_INCREMENT,
  `problem_id` int(10) unsigned NOT NUll,
  `user_id` int(10) unsigned NOT NULL,
  'date_subscriptions' datetime NULL
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
