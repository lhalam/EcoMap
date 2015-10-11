-- Created for gathering and controling permission for different type of users.
use ecomap;
DROP TABLE IF EXISTS  Permissions;

CREATE TABLE Permissions (
  id INT NOT NULL AUTO_INCREMENT,
  action ENUM('GET', 'PUT', 'POST', 'DELETE' ) NOT NULL,
  modifier ENUM('Any', 'Own', 'None'),
  resourses_id INT NOT NULL,
  PRIMARY KEY(id)
);
