-- Create the test database
CREATE DATABASE IF NOT EXISTS appdb_test
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- Grant privileges to appuser (assumes appuser is created by env vars)
GRANT ALL PRIVILEGES ON appdb_test.* TO 'appuser'@'%';
FLUSH PRIVILEGES;