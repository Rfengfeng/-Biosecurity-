DROP TABLE IF EXISTS StaffUser;

CREATE TABLE StaffUser (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_number INT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    address VARCHAR(255),
    work_phone_number VARCHAR(20),
    hire_date DATE DEFAULT (CURRENT_DATE),
    position VARCHAR(255),
    department VARCHAR(255),
    status ENUM('active', 'inactive') DEFAULT 'active',
    user_id INT,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES secureaccount(id)
);


INSERT INTO StaffUser (staff_number, first_name, last_name,  address, work_phone_number, hire_date, position, department, status, user_id)
VALUES (1, 'Admin', 'Admin', 'admin address', '1234567890', CURRENT_DATE, 'Admin', 'Admin Department', 'active', 28);


SELECT * FROM pythonlogin.staffuser;



DROP TABLE IF EXISTS RiverUser;

CREATE TABLE RiverUser (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    address VARCHAR(255),
    phone_number VARCHAR(20),
    date_joined DATE DEFAULT (CURRENT_DATE),
    status ENUM('active', 'inactive') DEFAULT 'active',
    user_id INT,
    CONSTRAINT fk_user_id_river  FOREIGN KEY (user_id) REFERENCES secureaccount(id)
);


INSERT INTO RiverUser (first_name, last_name, address,  phone_number, status, user_id)
VALUES ('user1', 'river', 'user Address',  '1234567890', 'active', 28);