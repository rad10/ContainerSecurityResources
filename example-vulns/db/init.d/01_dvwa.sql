-- Create a new database
CREATE DATABASE IF NOT EXISTS dvwa;

-- Create a new user
CREATE USER IF NOT EXISTS 'dvwa'@'%' IDENTIFIED BY 'p@ssw0rd';

-- Grant all privileges on the new database to the new user
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'%';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;