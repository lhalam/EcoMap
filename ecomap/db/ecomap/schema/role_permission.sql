CREATE TABLE IF NOT EXISTS role_permission (
  /*
  Simple table with relations between specific roles of users and its permissions.
  Permissions means activities of user what are allowed to do on site. User rights to edit status Problems entities
   */
  id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  role_id INT(10) UNSIGNED NOT NULL,
  permission_id INT(10) UNSIGNED NOT NULL,
  PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
