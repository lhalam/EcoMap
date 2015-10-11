# Should We use namespace here? Or we are
# going to pass it while executing code ?
DROP TABLE IF EXISTS Problem_activities;
CREATE TABLE Problem_activities (
    /*
        This table represents logging of all activities on
        exact problems.
    */
    id INT NOT NULL AUTO_INCREMENT,
    # Time of activity's occuring
    datetime TIMESTAMP NOT NULL,
    problem_id INT NOT NULL,
    user_id INT NOT NULL,
    activity_type ENUM('Added', 'Removed', 'Updated', 'Vote') NOT NULL,
    PRIMARY KEY (id)
);