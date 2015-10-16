DROP DATABASE IF EXISTS ecomap_db;

CREATE DATABASE ecomap_db;
use ecomap_db;

SOURCE schema/comment.sql;
SOURCE schema/detailed_problem.sql;
SOURCE schema/permission.sql;
SOURCE schema/photo.sql;
SOURCE schema/problem_activity.sql;
SOURCE schema/problem_type.sql;
SOURCE schema/problem.sql;
SOURCE schema/resource.sql;
SOURCE schema/role_permission.sql;
SOURCE schema/role.sql;
SOURCE schema/user_role.sql;
SOURCE schema/user.sql;
SOURCE schema/vote.sql;
