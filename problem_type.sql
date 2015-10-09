# Should We use namespace here? Or we are 
# going to pass it while executing code ?
DROP TABLE IF EXISTS Problem_type;
CREATE TABLE Problem_type (
    /*
        This table provides description of all problem types
    */
    id INT NOT NULL AUTO_INCREMENT,
    type VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);