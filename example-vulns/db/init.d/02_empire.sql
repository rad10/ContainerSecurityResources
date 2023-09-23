-- Create a new database
CREATE DATABASE IF NOT EXISTS empire;

-- Create a new user
CREATE USER IF NOT EXISTS 'empire'@'%' IDENTIFIED BY 'simplego422';

-- Grant all privileges on the new database to the new user
GRANT ALL PRIVILEGES ON empire.* TO 'empire'@'%';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;