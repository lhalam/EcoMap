-- Created for gathering and controling permission for different type of users.
CREATE TABLE IF NOT EXISTS permission (
  id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  action ENUM('GET', 'PUT', 'POST', 'DELETE' ) NOT NULL,
  modifier ENUM('Any', 'Own', 'None') NOT NULL DEFAULT 'None',
  resourses_id INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
