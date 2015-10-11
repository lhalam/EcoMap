use ecomap;
DROP TABLE IF EXISTS Roles;
CREATE TABLE Roles (
  id INT NOT NULL  AUTO_INCREMENT,
  name INT NOT NULL,              -- name of role
  PRIMARY KEY(id)
);