/*
    User_roles table create relations between users and their specific roles.
*/
CREATE TABLE IF NOT EXISTS user_role (
 id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
 user_id INT(10) UNSIGNED NOT NULL,
 roles_id INT(10) UNSIGNED NOT NULL,
 PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
