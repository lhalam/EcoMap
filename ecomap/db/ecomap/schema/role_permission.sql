/*
    Simple table with relations between specific
    roles of users and its permissions.
    Permissions means activities of user
    what are allowed to do on site.
    User rights to edit status Problems entities
*/
CREATE TABLE IF NOT EXISTS `role_permission` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `role_id` int(10) unsigned NOT NULL,
  `permission_id` int(10) unsigned NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;