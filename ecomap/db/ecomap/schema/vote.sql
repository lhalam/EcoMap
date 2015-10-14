CREATE TABLE IF NOT EXISTS vote (
  id INT(10) UNSIGNED NOT NULl AUTO_INCREMENT,
  problem_id INT(10) UNSIGNED NOT NUll, # problem, wich was voted
  user_id INT(10) UNSIGNED NOT NULL , # user who has voted
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
