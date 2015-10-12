CREATE TABLE Votes (
  id INT NOT NULl AUTO_INCREMENT,
  problem_id INT NOT NUll, # problem, wich was voted
  user_id INT NOT NULL , # user who has voted
  vote_value INT , # select value of severity
  PRIMARY KEY (id),
  FOREIGN KEY (problem_id) REFERENCES problem(id),
  FOREIGN KEY (user_id) REFERENCES user(id)
);