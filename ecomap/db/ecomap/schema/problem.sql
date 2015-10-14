CREATE TABLE IF NOT EXISTS problem (
 id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
 title VARCHAR(255) NOT NULL,
 content VARCHAR(255) NOT NULL,
 proposal VARCHAR(255) NOT NULL, /*User can propose a solution*/
 severity ENUM('1', '2', '3', '4', '5') NOT NULL DEFAULT '1',
 status ENUM('Solved', 'Unsolved') NOT NULL DEFAULT 'Unsolved', /* not resolved or resolved */
 latitude FLOAT NOT NULL,   # coordinats of
 longtitude FLOAT NOT NULL, # location
 problem_type_id ENUM('Forests', 'Landfill', 'Illegal_construction','Reservoirs',
                      'Biodiversity', 'Poaching', 'Other') NOT NULL,
 create_date INT(11) UNSIGNED NOT NULL, /*date of creation*/
 problem_types_id INT(10) UNSIGNED NOT NUll,
 user_id INT(10) UNSIGNED NOT NULL,
 PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;