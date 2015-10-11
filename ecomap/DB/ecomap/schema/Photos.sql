DROP TABLE IF EXISTS  Photos;
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
  PRIMARY KEY (id)
);
