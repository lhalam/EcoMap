CREATE TABLE IF NOT EXISTS comment (
  id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  content VARCHAR(255) NOT NULL,
  problem_id INT(10) UNSIGNED NOT NULL,         -- problem, comment belongs to
  user_id INT(10) UNSIGNED NOT NULL,            -- user, comment belongs to
  created_date INT(11) UNSIGNED NOT NULL,         -- date of create
  update_date INT(11) UNSIGNED NULL, 
  modified_date INT(11) UNSIGNED NULL,            -- date, when comment was modified
  modified_user_id INT(10) UNSIGNED NULL,       -- user, who modified comment
  PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
