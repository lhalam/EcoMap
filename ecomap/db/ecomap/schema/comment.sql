/*
    This table stands for holding comments
    of problems and information about those
    comments.
*/
CREATE TABLE IF NOT EXISTS `comment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` varchar(255) NOT NULL,
  `problem_id` int(10) unsigned NOT NULL,     # problem, comment belongs to
  `user_id` int(10) unsigned NOT NULL,        # user, comment belongs to
  `created_date` int(11) unsigned NOT NULL,   # date of create
  `updated_date` int(11) unsigned NULL,
  `modified_date` int(11) unsigned NULL,      # date, when comment was modified
  `modified_user_id` int(10) unsigned NULL,   # user, who modified comment
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
