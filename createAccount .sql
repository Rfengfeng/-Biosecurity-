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
('pest', 'yes', 'Koi Carp', 'Cyprinus carpio', 'Large scales, barbels at the corners of the mouth', 'Koi carp is an invasive fish species known for its large size and disruptive feeding behavior. It competes with native fish for food and habitat, leading to declines in native species populations. Additionally, koi carp can increase water turbidity and promote algal growth, affecting water quality.', 'Displacement of native fish species, degradation of aquatic habitats, altered nutrient cycling', NULL),
('disease', 'yes', 'Didymo', 'Didymosphenia geminata', 'Thick brown mats, often mistaken for sewage pollution', 'Didymo, also known as "rock snot," is a type of freshwater algae that forms thick brown mats on riverbeds and rocks. It can smother aquatic vegetation and disrupt ecosystems by altering water flow patterns and reducing habitat quality for native species.', 'Reduction in biodiversity, altered ecosystem structure, impacts on recreational activities such as fishing', NULL),
('pest', 'yes', 'Asian Clam', 'Corbicula fluminea', 'Small, triangular shell with distinct concentric ridges', 'The Asian clam is an invasive bivalve mollusk that has spread to freshwater habitats around the world. It reproduces rapidly and can reach high population densities, outcompeting native species for resources. Asian clams also alter nutrient cycling and can contribute to algal blooms.', 'Displacement of native mollusk species, alteration of benthic communities, impacts on water quality', NULL),
('disease', 'yes', 'Myrtle Rust', 'Austropuccinia psidii', 'Yellow or orange spore masses on leaves, stems, or fruit', 'Myrtle rust is a fungal disease that affects plants in the myrtle family, including pohutukawa, feijoa, and manuka. It spreads through spores and can rapidly defoliate susceptible plants, leading to reduced growth and reproductive capacity. Myrtle rust poses a significant threat to New Zealands native ecosystems and horticultural industries.', 'Defoliation of native plants, impacts on ecosystem function, economic losses for horticulture', NULL),
('pest', 'yes', 'Gambusia', 'Gambusia affinis', 'Upturned mouth, elongated body, dark vertical stripes', 'Gambusia, also known as mosquitofish, is a small freshwater fish introduced to control mosquito populations. However, it has become invasive in many regions, preying on native fish and amphibian larvae. Gambusia can disrupt aquatic food webs and reduce biodiversity in freshwater habitats.', 'Predation on native species, competition for resources, impacts on ecosystem stability', NULL),
('disease', 'yes', 'Didymo', 'Didymosphenia geminata', 'Thick brown mats, often mistaken for sewage pollution', 'Didymo, also known as "rock snot," is a type of freshwater algae that forms thick brown mats on riverbeds and rocks. It can smother aquatic vegetation and disrupt ecosystems by altering water flow patterns and reducing habitat quality for native species.', 'Reduction in biodiversity, altered ecosystem structure, impacts on recreational activities such as fishing', NULL),
('pest', 'yes', 'Starry Stonewort', 'Nitellopsis obtusa', 'Stringy, star-shaped algae with bulbils', 'Starry stonewort is a type of filamentous green alga that forms dense mats in freshwater lakes and rivers. It can outcompete native aquatic plants and disrupt ecosystems by altering habitat structure and nutrient cycling. Starry stonewort is difficult to control once established and can negatively impact water quality and recreational activities.', 'Displacement of native vegetation, alteration of aquatic habitats, impacts on recreational use', NULL),
('disease', 'yes', 'Cyanobacterial Blooms', 'Various species', 'Green, blue, or red scums on the water surface', 'Cyanobacterial blooms are caused by the rapid growth of cyanobacteria in freshwater bodies. These blooms can produce toxins that are harmful to humans and aquatic organisms. Cyanobacterial blooms are often associated with nutrient pollution and can result in fish kills, ecosystem degradation, and health risks for humans and animals.', 'Toxicity to aquatic life, health risks to humans and animals, ecosystem disruption', NULL),
('pest', 'yes', 'Giant Salvinia', 'Salvinia molesta', 'Floating aquatic fern with distinctive eggbeater-shaped leaves', 'Giant salvinia is a highly invasive aquatic plant that forms dense mats on the water surface, choking out native vegetation and reducing oxygen levels. It can clog waterways, disrupt aquatic ecosystems, and impede recreational activities such as boating and fishing. Giant salvinia is difficult to control and can spread rapidly under favorable conditions.', 'Habitat degradation, displacement of native species, impacts on water quality', NULL),
('disease', 'yes', 'Kauri Dieback', 'Phytophthora agathidicida', 'Yellowing leaves, trunk lesions, gum bleeding', 'Kauri dieback is a serious fungal disease that affects kauri trees, iconic to New Zealand forests. It spreads through soil movement and infects the roots of kauri trees, eventually leading to tree death. The disease has devastated kauri populations in many parts of New Zealand and poses a significant threat to the survival of these iconic trees.', 'Mortality of kauri trees, loss of biodiversity, impacts on ecosystem function', NULL),
('pest', 'yes', 'Red Swamp Crayfish', 'Procambarus clarkii', 'Bright red coloration, raised claws', 'The red swamp crayfish is an invasive freshwater crustacean native to North America. It has been introduced to various regions around the world for aquaculture and as a food source. However, red swamp crayfish can outcompete native species, disrupt aquatic ecosystems, and cause damage to irrigation systems and water infrastructure.', 'Predation on native species, habitat alteration, impacts on water quality', NULL),
('disease', 'yes', 'Phytophthora Agathidicida', 'Phytophthora agathidicida', 'Yellowing leaves, trunk lesions, gum bleeding', 'Phytophthora agathidicida is the causal agent of kauri dieback disease, a serious threat to kauri trees in New Zealand. It infects the roots of kauri trees, leading to rot and eventual death. The disease can spread through soil movement and poses a significant risk to kauri forests and ecosystems.', 'Mortality of kauri trees, loss of biodiversity, impacts on ecosystem function', NULL);


-- Insert 8 freshwater pests/diseases not present in NZ
INSERT INTO freshwater_guide (freshwater_item_type, present_in_NZ, common_name, scientific_name, key_characteristics, biology_description, impacts, primary_image) VALUES
('pest', 'no', 'Snakehead Fish', 'Channa spp.', 'Freshwater predatory fish with distinctive snake-like appearance', 'Snakehead fish are predatory fish native to parts of Asia and Africa. They have the ability to breathe air and can survive out of water for extended periods, posing a threat to native ecosystems if introduced.', 'Predation on native fish species, disruption of ecosystems', NULL),
('disease', 'no', 'Crayfish Plague', 'Aphanomyces astaci', 'Pathogen affecting freshwater crayfish', 'Crayfish plague is a disease caused by the water mold Aphanomyces astaci, which infects and kills freshwater crayfish. It can spread rapidly in crayfish populations and has led to declines in native crayfish species in some areas.', 'Population declines of native crayfish species', NULL);
-- Add more pests/diseases not present in NZ here...