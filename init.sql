-- =======================================================
-- AI Smart Citizen Grievance System Database Initialization
-- =======================================================

-- 1. Citizens Table
CREATE TABLE IF NOT EXISTS citizens (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    city VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- 2. Complaints Table
CREATE TABLE IF NOT EXISTS complaints (
    id SERIAL PRIMARY KEY,
    citizen_id INT REFERENCES citizens(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    department VARCHAR(50) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending'
);

-- 3. Officers Table
CREATE TABLE IF NOT EXISTS officers (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    department VARCHAR(50) NOT NULL
);

-- -------------------------------------------------------
-- SEED INITIAL DATA
-- -------------------------------------------------------

-- Seed Registered Citizens
INSERT INTO citizens (id, name, age, city, phone, email) VALUES
(1, 'Naman Sharma', 25, 'New Delhi', '9876543210', 'naman@example.com'),
(2, 'Deepanshu Sharma', 30, 'Mumbai', '9876543211', 'deepanshu@example.com'),
(3, 'Himani Sharma', 28, 'Bangalore', '9876543212', 'himani@example.com'),
(4, 'Piyush Kumar', 23, 'Bulandshahar', '9876543213', 'piyush@example.com'),
(5, 'Chirag Patel', 22, 'Ahmedabad', '9876543214', 'chirag@example.com')
ON CONFLICT (id) DO NOTHING;

-- Reset sequence for citizens table so next inserts get id >= 6
SELECT setval('citizens_id_seq', (SELECT COALESCE(MAX(id), 1) FROM citizens));

-- Seed Officers for all 5 departments (Default Password for all: admin123)
-- bcrypt hash for 'admin123': $2b$12$iLffLZgi/88TbzSjaqyLU.P1C2glEM58Nwsm8tmmF8FzGQff3gKaO
INSERT INTO officers (username, password, department) VALUES
('municipal_admin', '$2b$12$iLffLZgi/88TbzSjaqyLU.P1C2glEM58Nwsm8tmmF8FzGQff3gKaO', 'municipal'),
('water_admin', '$2b$12$iLffLZgi/88TbzSjaqyLU.P1C2glEM58Nwsm8tmmF8FzGQff3gKaO', 'water'),
('electricity_admin', '$2b$12$iLffLZgi/88TbzSjaqyLU.P1C2glEM58Nwsm8tmmF8FzGQff3gKaO', 'electricity'),
('gas_admin', '$2b$12$iLffLZgi/88TbzSjaqyLU.P1C2glEM58Nwsm8tmmF8FzGQff3gKaO', 'gas'),
('transport_admin', '$2b$12$iLffLZgi/88TbzSjaqyLU.P1C2glEM58Nwsm8tmmF8FzGQff3gKaO', 'transport')
ON CONFLICT (username) DO NOTHING;

-- Seed Sample Grievances for Dashboard display
INSERT INTO complaints (citizen_id, description, department, priority, status) VALUES
(1, 'Severe underground water pipeline burst near street 4 causing dirty tap water.', 'water', 'High', 'Pending'),
(2, 'Frequent voltage fluctuations and blown transformer in commercial block B.', 'electricity', 'High', 'In Progress'),
(3, 'Garbage accumulation near market square and broken street lamp on corner.', 'municipal', 'Medium', 'Pending'),
(4, 'Smell of LPG gas leakage near residential distribution pipe.', 'gas', 'High', 'Resolved'),
(5, 'Morning peak bus service on Route 21 consistently skipped for 3 days.', 'transport', 'Low', 'Pending')
ON CONFLICT DO NOTHING;
