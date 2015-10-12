CREATE TABLE Problem (
  id INT NOT NULl AUTO_INCREMENT,
  content VARCHAR(255) NOT NULL , 
  proposal VARCHAR(255) NOT NULL , # propose the solution
  severity VARCHAR(255) , # seriousness of problem
  detailed_problem_id INT NOT NULL, 
  problem_types_id INT NOT NUll,
  PRIMARY KEY (id),
  FOREIGN KEY (detailed_problem_id) REFERENCES detailed_problem(id),
  FOREIGN KEY (problem_types_id) REFERENCES problem_type(id)
);