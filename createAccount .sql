CREATE DATABASE `biosecurity`;
USE`biosecurity`;

DROP TABLE IF EXISTS secureaccount;

-- 创建 secureaccount 表
CREATE TABLE secureaccount (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff', 'RiverUser') NOT NULL
);

-- 添加五条记录
INSERT INTO secureaccount (username, password, email, role) VALUES
('admin1', 'password1', 'admin1@example.com', 'admin'),
('staff1', 'password2', 'staff1@example.com', 'staff'),
('staff2', 'password3', 'staff2@example.com', 'staff'),
('staff3', 'password3', 'staff3@example.com', 'staff'),
('user1', 'password4', 'user1@example.com', 'RiverUser'),
('user2', 'password4', 'user1@example.com', 'RiverUser'),
('user3', 'password4', 'user1@example.com', 'RiverUser'),
('user4', 'password4', 'user1@example.com', 'RiverUser'),
('user5', 'password5', 'user2@example.com', 'RiverUser');


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
    user_id INT
);


INSERT INTO StaffUser (staff_number, first_name, last_name,  address, work_phone_number, hire_date, position, department, status, user_id)
VALUES (1, 'Admin', 'Admin', 'admin address', '1234567890', CURRENT_DATE, 'Admin', 'Admin Department', 'active', 2);


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
    user_id INT
);


INSERT INTO RiverUser (first_name, last_name, address,  phone_number, status, user_id)
VALUES ('user1', 'river', 'user Address',  '1234567890', 'active', 5);



DROP TABLE IF EXISTS freshwater_guide;

CREATE TABLE freshwater_guide (
    freshwater_id INT AUTO_INCREMENT PRIMARY KEY,
    freshwater_item_type ENUM('pest', 'disease'),
    present_in_NZ ENUM('yes', 'no'),
    common_name VARCHAR(100),
    scientific_name VARCHAR(100),
    key_characteristics TEXT,
    biology_description TEXT,
    impacts TEXT,
    primary_image LONGBLOB
);



-- Insert 12 freshwater pests/diseases present in NZ
INSERT INTO freshwater_guide (freshwater_item_type, present_in_NZ, common_name, scientific_name, key_characteristics, biology_description, impacts, primary_image) VALUES
('pest', 'yes', 'Kauri Dieback', 'Phytophthora agathidicida', 'Pathogen affecting kauri trees', 'Kauri dieback is a serious disease of kauri trees, causing significant dieback of infected trees.', 'Loss of kauri trees, disruption of forest ecosystems', NULL),
('disease', 'yes', 'Didymo', 'Didymosphenia geminata', 'Aquatic invasive species forming large mats', 'Didymo is an invasive freshwater alga that forms thick mats on river bottoms, altering aquatic habitats and affecting native species.', 'Altered ecosystems, decreased biodiversity', NULL);
-- Add more pests/diseases present in NZ here...

-- Insert 8 freshwater pests/diseases not present in NZ
INSERT INTO freshwater_guide (freshwater_item_type, present_in_NZ, common_name, scientific_name, key_characteristics, biology_description, impacts, primary_image) VALUES
('pest', 'no', 'Snakehead Fish', 'Channa spp.', 'Freshwater predatory fish with distinctive snake-like appearance', 'Snakehead fish are predatory fish native to parts of Asia and Africa. They have the ability to breathe air and can survive out of water for extended periods, posing a threat to native ecosystems if introduced.', 'Predation on native fish species, disruption of ecosystems', NULL),
('disease', 'no', 'Crayfish Plague', 'Aphanomyces astaci', 'Pathogen affecting freshwater crayfish', 'Crayfish plague is a disease caused by the water mold Aphanomyces astaci, which infects and kills freshwater crayfish. It can spread rapidly in crayfish populations and has led to declines in native crayfish species in some areas.', 'Population declines of native crayfish species', NULL);
-- Add more pests/diseases not present in NZ here...