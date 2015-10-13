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