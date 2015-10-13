DROP TABLE IF EXISTS  Role_permissions;
CREATE TABLE Role_permissions (
  /*
  Simple table with relations between specific roles of users and its permissions.
  Permissions means activities of user what are allowed to do on site. User rights to edit status Problems entities
   */
  id INT NOT NULL AUTO_INCREMENT primary key,
  roles_id INT,
  permissions_id INT
);