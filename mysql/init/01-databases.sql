# create databases
CREATE DATABASE IF NOT EXISTS `db`;
CREATE DATABASE IF NOT EXISTS `test_db`;

# create user and grant rights
CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL ON db.* TO 'user'@'%';
GRANT ALL ON test_db.* TO 'user'@'%';