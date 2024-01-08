-- Inserting sample data into 'users' table
--INSERT INTO users (Name, Email, Company) VALUES
--('Henry Hill', 'henry.hill@example.com', 'self'),
--('Paulie Walnuts', 'paulie.walnuts@example.com', 'DiMeo');

-- Inserting sample data into 'products' table
INSERT INTO products (ProductName, Description) VALUES 
('Flux Capacitor', 'For capacitation throughout time'),
('Tardis', 'Its bigger on the inside')

-- Assuming your licenses table uses a string format for LicenseKey
-- Inserting sample data into 'licenses' table
INSERT INTO licenses (LicenseKey, ProductID, UserID, ExpiryDate, IsActive) VALUES 
('ABC123', 1, 1, '2024-12-31', TRUE),
('XYZ789', 2, 2, '2024-12-31', TRUE);
