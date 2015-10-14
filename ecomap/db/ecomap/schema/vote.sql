CREATE TABLE IF NOT EXISTS `vote` (
  `id` int(10) unsigned NOT NULl AUTO_INCREMENT,
  `problem_id` int(10) unsigned NOT NUll, # problem, wich was voted
  `user_id` int(10) unsigned NOT NULL ,   # user who has voted
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
