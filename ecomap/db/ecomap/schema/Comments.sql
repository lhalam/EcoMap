DROP TABLE IF EXISTS  Comments;
CREATE TABLE Comments (
  id INT NOT NULl AUTO_INCREMENT,
  content VARCHAR(255) NOT NULL,
  problem_id INT NOT NULL,         -- problem, comment belongs to
  user_id INT NOT NULL,            -- user, comment belongs to
  created_date DATETIME NOT NULL,         -- date of create
  modified_date DATETIME NULL,            -- date, when comment was modified
  modified_user_id INT NULL,       -- user, who modified comment
  PRIMARY KEY(id)
);
