/*
    Table for storage attached photos to Problem entities.
    Has reference
      :on user_id -> a user, who attached the photo
      :on problem_id -> specific Problem entity which photos belongs to
*/
CREATE TABLE IF NOT EXISTS `photo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,     # each photo must have unique name according to it /PATH/name.jpg
  `description` varchar(255),  # this textfield type might be changed
  `problem_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
