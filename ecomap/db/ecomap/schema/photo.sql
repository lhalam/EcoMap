CREATE TABLE IF NOT EXISTS photo (
  /*
  Table for storage attached photos to Problem entities.
  Has reference
    :on user_id -> a user, who attached the photo
    :on problem_id -> specific Problem entity which photos belongs to
 */
  id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE, # each photo must have unique name according to it /PATH/name.jpg
  description VARCHAR(255) NULL, # this textfield type might be changed
  problem_id INT(11) UNSIGNED NOT NULL,
  user_id INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
