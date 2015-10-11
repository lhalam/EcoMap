DROP DATABASE IF EXISTS ecomap;

CREATE DATABASE ecomap
CHARACTER SET utf8 COLLATE utf8_general_ci;
use ecomap;
# DROP TABLE IF EXISTS  Users;
-- Table created for gathering information about user for transfering to another tables
CREATE TABLE  if not exists Users (
  id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL,
  PRIMARY KEY(id)
);

# DROP TABLE IF EXISTS  Resources;
CREATE TABLE Resources (
  id INT NOT NULL,
  resource_name VARCHAR(100) NOT NULL,    -- name of resource
  PRIMARY KEY(id)
);

# DROP TABLE IF EXISTS  Permissions;
CREATE TABLE Permissions (
  id INT NOT NULL AUTO_INCREMENT,
  action ENUM('GET', 'PUT', 'POST', 'DELETE' ) NOT NULL,
  modifier ENUM('Any', 'Own', 'None'),
  resourses_id INT NOT NULL,
  PRIMARY KEY(id)
);

# DROP TABLE IF EXISTS  Roles;
CREATE TABLE Roles (
  id INT NOT NULL,
  name INT NOT NULL,              -- name of role
  PRIMARY KEY(id)
);

	/*
	User_roles table create relations between users and their specific roles.
	*/
# DROP TABLE IF EXISTS  User_roles;
CREATE TABLE User_roles (
 id INT NOT NULL AUTO_INCREMENT,
 user_id INT NOT NULL,
 roles_id INT NOT NULL,
 PRIMARY KEY (id),
 FOREIGN KEY (user_id) REFERENCES Users(id),
 FOREIGN KEY (roles_id) REFERENCES Roles(id)
);

# DROP TABLE IF EXISTS  Role_permissions;
CREATE TABLE Role_permissions (
  /*
  Simple table with relations between specific roles of users and its permissions.
  Permissions means activities of user what are allowed to do on site. User rights to edit status Problems entities
   */
  id INT NOT NULL AUTO_INCREMENT primary key,
  roles_id INT,
  permissions_id INT,
  FOREIGN KEY (roles_id) REFERENCES Roles(id),
  FOREIGN KEY (permissions_id) REFERENCES Permissions(id)
);

# DROP TABLE IF EXISTS  Detailed_problems;
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

# Should We use namespace here? Or we are
# going to pass it while executing code ?
# DROP TABLE IF EXISTS Problem_types;
CREATE TABLE Problem_types (
    /*
        This table provides description of all problem types
    */
    id INT NOT NULL AUTO_INCREMENT,
    type VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);


# DROP TABLE IF EXISTS  Problems;
CREATE TABLE Problems (
  id INT NOT NULl AUTO_INCREMENT,
  content VARCHAR(255) NOT NULL ,
  proposal VARCHAR(255) NOT NULL , # propose the solution
  severity ENUM('1', '2', '3', '4', '5') NOT NULL DEFAULT 1, # seriousness of problem
  detailed_problem_id INT NOT NULL,
  problem_types_id INT NOT NUll,
  PRIMARY KEY (id),
  FOREIGN KEY (detailed_problem_id) REFERENCES Detailed_problems(id),
  FOREIGN KEY (problem_types_id) REFERENCES Problem_types(id)
);

# Should We use namespace here? Or we are
# going to pass it while executing code ?
# DROP TABLE IF EXISTS Problem_activities;
CREATE TABLE Problem_activities (
    /*
        This table represents logging of all activities on
        exact problems.
    */
    id INT NOT NULL AUTO_INCREMENT,
    # Time of activity's occuring
    datetime TIMESTAMP NOT NULL,
    problem_id INT NOT NULL,
    user_id INT NOT NULL,
    activity_type ENUM('Added', 'Removed', 'Updated', 'Vote') NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (problem_id) REFERENCES Problems(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

# DROP TABLE IF EXISTS  Votes;
CREATE TABLE Votes (
  id INT NOT NULl AUTO_INCREMENT,
  problem_id INT NOT NUll, # problem, wich was voted
  user_id INT NOT NULL , # user who has voted
  vote_value INT , # select value of severity
  PRIMARY KEY (id),
  FOREIGN KEY (problem_id) REFERENCES Problems(id),
  FOREIGN KEY (user_id) REFERENCES Users(id)
);

# DROP TABLE IF EXISTS  Photos;
CREATE TABLE Photos (
  /*
  Table for storage attached photos to Problem entities.
  Has reference
    :on user_id -> a user, who attached the photo
    :on problem_id -> specific Problem entity which photos belongs to
 */
  id INT NOT NULL AUTO_INCREMENT, # MEDIUMINT for secure incrementation :) or just regular INT ?
  Name VARCHAR(255) NOT NULL UNIQUE, # each photo must have unique name according to it /PATH/name.jpg
  Description LONGTEXT NULL, # this textfield type might be changed
  problem_id INT,
  user_id INT,
  PRIMARY KEY (id),
  FOREIGN KEY (problem_id) REFERENCES Problems(id),
  FOREIGN KEY (user_id) REFERENCES Users(id)
);

# DROP TABLE IF EXISTS  Comments;
CREATE TABLE Comments (
  id INT NOT NULl AUTO_INCREMENT,
  content VARCHAR(255) NOT NULL,
  problem_id INT NOT NULL,         -- problem, comment belongs to
  user_id INT NOT NULL,            -- user, comment belongs to
  created_date DATETIME NOT NULL,         -- date of create
  modified_date DATETIME NULL,            -- date, when comment was modified
  modified_user_id INT NULL,       -- user, who modified comment
  PRIMARY KEY(id),
  FOREIGN KEY(problem_id) REFERENCES Problems(id),
  FOREIGN KEY(user_id) REFERENCES Users(id)
);
