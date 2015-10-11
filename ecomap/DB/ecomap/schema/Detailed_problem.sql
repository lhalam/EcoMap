use ecomap;
DROP TABLE IF EXISTS  Detailed_problems;
CREATE TABLE Detailed_problems (
id INT NOT NULL AUTO_INCREMENT,
 title VARCHAR(255) NOT NULL,
 content VARCHAR(255) NOT NULL,
 proposal VARCHAR(255) NOT NULL, /*User can propose a solution*/
 severity ENUM('1', '2', '3', '4', '5') NOT NULL DEFAULT 1,
 status ENUM('Solved', 'Unsolved') NOT NULL DEFAULT 'Unsolved', /* not resolved or resolved */
 location DOUBLE NOT NULL, /*Latitude and Longtitude of the problem*/
 problem_type_id ENUM('Forests', 'Landfill', 'Illegal_construction','Reservoirs',
                      'Biodiversity', 'Poaching', 'Other') NOT NULL,
 number_of_votes INT DEFAULT 0,
 datetime TIMESTAMP NOT NULL, /*date of create*/
 first_name VARCHAR(100) NOT NULL,
 last_name VARCHAR(100) NOT NULL,
 number_of_comments INT,
 PRIMARY KEY (id)
);