CREATE TABLE IF NOT EXISTS problem_type (
    /*
        This table provides description of all problem types
    */
    id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    type VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
