	/*
	User_roles table create relations between users and their specific roles.
	*/
use ecomap;
DROP TABLE IF EXISTS  User_roles;
CREATE TABLE User_roles (
 id INT NOT NULL AUTO_INCREMENT,
 user_id INT NOT NULL,
 roles_id INT NOT NULL,
 PRIMARY KEY (id)
);