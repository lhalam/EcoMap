/*
    User_roles table create relations
    between users and their specific
    roles.
*/
CREATE TABLE IF NOT EXISTS `user_role` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
 `user_id` int(10) unsigned NOT NULL,
 `role_id` int(10) unsigned NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
