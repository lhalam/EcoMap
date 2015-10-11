DROP TABLE IF EXISTS  Problems;
CREATE TABLE Problems (
  id INT NOT NULl AUTO_INCREMENT,
  content VARCHAR(255) NOT NULL ,
  proposal VARCHAR(255) NOT NULL , # propose the solution
  severity ENUM('1', '2', '3', '4', '5') NOT NULL DEFAULT 1, # seriousness of problem
  detailed_problem_id INT NOT NULL,
  problem_types_id INT NOT NUll,
  PRIMARY KEY (id)
);
