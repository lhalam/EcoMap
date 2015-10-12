	/*
	User_roles table create relations between users and their specific roles.
	*/
CREATE TABLE User_roles (
 id INT NOT NULL AUTO_INCREMENT,
 user_id INT NOT NULL,
 roles_id INT NOT NULL,
 PRIMARY KEY (id),
 FOREIGN KEY (user_id) REFERENCES User(id),
 FOREIGN KEY (roles_id) REFERENCES Roles(id)
);

