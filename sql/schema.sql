-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Company VARCHAR(255)
);

-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    Description TEXT
);

-- Create Licenses Table
CREATE TABLE IF NOT EXISTS licenses (
    LicenseKey VARCHAR(255) PRIMARY KEY,
    ProductID INT NOT NULL,
    UserID INT NOT NULL,
    ExpiryDate DATE NOT NULL,
    IsActive BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);

-- Create Event Logs Table
CREATE TABLE IF NOT EXISTS event_logs (
    LogID VARCHAR(255) PRIMARY KEY,
    Timestamp DATETIME NOT NULL,
    FunctionName VARCHAR(255) NOT NULL,
    EventType VARCHAR(50) NOT NULL,
    Message TEXT,
    AdditionalInfo TEXT
);
