CREATE DATABASE IF NOT EXISTS qc_audit_db;
USE qc_audit_db;

-- Table to store logged errors
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    auditor_name VARCHAR(100) NOT NULL,
    error_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data to populate the dashboard immediately
INSERT INTO audit_logs (team_name, auditor_name, error_type, status) VALUES
('Team Cl', 'Suresh', 'Data Entry Error', 'Resolved'),
('Team Gatekeeping', 'Suresh', 'Compliance Miss', 'Pending'),
('Team Isc transportation', 'Ramesh', 'Documentation Error', 'Pending'),
('Team Pl', 'Suresh', 'Data Entry Error', 'Resolved'),
('Team Cl', 'Ramesh', 'Data Entry Error', 'Resolved');