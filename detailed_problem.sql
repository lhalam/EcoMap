CREATE TABLE Detailed_problem (
 id INT NOT NULL,
 title VARCHAR(255) NOT NULL, 
 content VARCHAR(255) NOT NULL,
 proposal VARCHAR(255) NOT NULL, /*User can propose a solution*/
 severity ENUM('1', '2', '3', '4', '5') NOT NULL,
 status ENUM('Solved', 'Unsolved') NOT NULL, /* not resolved or resolved */
 location BIGINT NOT NULL, /*Latitude and Longtitude of the problem*/
 problem_type_id ENUM('Forests', 'Landfill', 'Illegal_construction','Reservoirs', 'Biodiversity', 'Poaching', 'Other') NOT NULL,
 number_of_votes INT,
 datetime TIMESTAMP NOT NULL, /*date of create*/
 first_name VARCHAR(100) NOT NULL,
 last_name VARCHAR(100) NOT NULL,
 number_of_comments INT,
 PRIMARY KEY (id),
);
