use ecomap;
ALTER TABLE Permissions
  ADD FOREIGN KEY (resourses_id) REFERENCES Resources(id);

ALTER TABLE User_roles
  ADD FOREIGN KEY (roles_id) REFERENCES Roles(id);

ALTER TABLE Role_permissions
  ADD FOREIGN KEY (roles_id) REFERENCES Roles(id),
  ADD FOREIGN KEY (permissions_id) REFERENCES Permissions(id);

ALTER TABLE Problems
  ADD FOREIGN KEY (detailed_problem_id) REFERENCES Detailed_problems(id),
  ADD FOREIGN KEY (problem_types_id) REFERENCES Problem_types(id);

ALTER TABLE Problem_activities
  ADD FOREIGN KEY (problem_id) REFERENCES Problems(id),
  ADD FOREIGN KEY (user_id) REFERENCES Users(id);

ALTER TABLE Votes
  ADD FOREIGN KEY (problem_id) REFERENCES Problems(id),
  ADD FOREIGN KEY (user_id) REFERENCES Users(id);

ALTER TABLE Photos
  ADD FOREIGN KEY (problem_id) REFERENCES Problems(id),
  ADD FOREIGN KEY (user_id) REFERENCES Users(id);

ALTER TABLE Comments
  ADD FOREIGN KEY (problem_id) REFERENCES Problems(id),
  ADD FOREIGN KEY (user_id) REFERENCES Users(id);


INSERT INTO Problem_types(type)
VALUES ('first problem type');

INSERT INTO Users (first_name, last_name, email, password)
VALUES ('vadim', 'padalko', '22@mail.ru', 'pass');

INSERT INTO Detailed_problems(title, content, proposal, severity, status,
            location, problem_type_id, number_of_votes, datetime, first_name, last_name, number_of_comments)
VALUES ('title1', 'cont1', 'prop1', 1, 'Unsolved',1243.33434,'Forests',0,now(),'firstname','lastname',0);

INSERT INTO Problems(content, proposal, severity, detailed_problem_id, problem_types_id)
VALUES ('content probl1', 'my proposal',5, 1, 1);
