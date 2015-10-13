DROP DATABASE IF EXISTS ecomap_db;

CREATE DATABASE ecomap_db;
use ecomap_db;

SOURCE schema/Comments.sql;
SOURCE schema/Detailed_problem.sql;
SOURCE schema/Permissions.sql;
SOURCE schema/Photos.sql;
SOURCE schema/Problem_activities.sql;
SOURCE schema/Problem_types.sql;
SOURCE schema/Problems.sql;
SOURCE schema/Resources.sql;
SOURCE schema/Role_permissions.sql;
SOURCE schema/Roles.sql;
SOURCE schema/User_roles.sql;
SOURCE schema/Users.sql;
SOURCE schema/Votes.sql;
SOURCE schema/Foreign_keys.sql;
