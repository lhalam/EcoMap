/* 
    This table has info that is gathering 
    and controling permission for different
    type of users.
*/
CREATE TABLE IF NOT EXISTS `permission` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `action` enum('GET', 'PUT', 'POST', 'DELETE' ) NOT NULL,
  `modifier` enum('Any', 'Own', 'None') NOT NULL DEFAULT 'None',
  `resource_id` int(10) unsigned NOT NULL,
  `role_id` int(10) unsigned NOT NULL,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
