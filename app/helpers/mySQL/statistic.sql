USE mad;

CREATE TABLE tblStatisticType (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    unit VARCHAR(50) NOT NULL
);

CREATE TABLE tblStatisticData (
    id INT AUTO_INCREMENT PRIMARY KEY,
    statisticTypeId INT NOT NULL,
    value FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (statisticTypeId) REFERENCES tblStatisticType(id) ON DELETE CASCADE
);
