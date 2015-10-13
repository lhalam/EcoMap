DROP TABLE IF EXISTS  Resources;
CREATE TABLE Resources (
  id INT NOT NULL,
  resource_name VARCHAR(100) NOT NULL,    -- name of resource
  PRIMARY KEY(id)
);