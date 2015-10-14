CREATE TABLE IF NOT EXISTS page (
  id INT(10) UNSIGNED NOT NULl AUTO_INCREMENT,
  alias VARCHAR(100) NOT NUll, # problem, wich was voted
  title VARCHAR(100) NOT NULL , # user who has voted
  description VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  meta_keywords VARCHAR(255) NULL,
  meta_desription VARCHAR(255) NULL,
  is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
