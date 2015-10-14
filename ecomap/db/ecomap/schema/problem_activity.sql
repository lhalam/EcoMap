CREATE TABLE IF NOT EXISTS problem_activity (
    /*
        This table represents logging of all activities on
        exact problems.
    */
    id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    # Time of activity's occuring
    create_date INT(11) UNSIGNED NOT NULL,
    problem_id INT(10) UNSIGNED NOT NULL,
    user_id INT(10) UNSIGNED NOT NULL,
    activity_type ENUM('Added', 'Removed', 'Updated', 'Vote') NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
