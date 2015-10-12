-- Created for gathering and controling permission for different type of users.
CREATE TABLE ecomap.permissions
(id INT NOT NULL AUTO_INCREMENT,
action VARCHAR(100) NOT NULL,
modifier VARCHAR(100) NOT NULL,
resourses_id INT NOT NULL,
FOREIGN KEY (resourses_id) REFERENCES Resourses(id),
PRIMARY KEY(id));

