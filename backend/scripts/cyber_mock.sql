CREATE TABLE IF NOT EXISTS Cyber_Evidence (
    EvidenceID INT AUTO_INCREMENT PRIMARY KEY,
    FIRNumber VARCHAR(50),
    IPAddress VARCHAR(50),
    CrimeType VARCHAR(100)
);

INSERT INTO Cyber_Evidence (FIRNumber, IPAddress, CrimeType) VALUES
('FIR-2026-001', '8.8.8.8', 'DDoS Attack'),
('FIR-2026-002', '1.1.1.1', 'Phishing Campaign'),
('FIR-2026-003', '93.184.216.34', 'Data Exfiltration');
