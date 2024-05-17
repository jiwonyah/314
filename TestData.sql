/* 100 UserAccount */
WITH RECURSIVE
  cnt(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM cnt WHERE x < 100)
INSERT INTO user (userid, password, email, firstName, lastName, role, status)
SELECT 
  'user' || x, 
  '$2y$10$H2/azUTKrhE3rP.BBoAi6.tVyumH.qkAOiTwmF7ZxrgsdzUK0CDfK', -- bcrpted version of 'testpassword'
  'user' || x || '@example.com', 
  'First' || x, 
  'Last' || x, 
  CASE 
    WHEN x = 1 THEN 'admin'
    WHEN (x - 2) % 3 = 0 THEN 'buyer'
    WHEN (x - 3) % 3 = 0 THEN 'seller'
    ELSE 'agent'
  END, 
  'Active'
FROM cnt;



/* 4 UserProfile */
INSERT INTO profile (profileName, profileDescription, status) VALUES
('admin', 'Administrator profile', 'Active'),
('buyer', 'Buyer profile', 'Active'),
('seller', 'Seller profile', 'Active'),
('agent', 'Agent profile', 'Active');



/* 100 PropertyListings */
WITH RECURSIVE
  cnt(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM cnt WHERE x < 100)
INSERT INTO propertyListing (
    subject, 
    price, 
    address, 
    floorSize, 
    floorLevel, 
    propertyType, 
    furnishing, 
    builtYear, 
    create_date, 
    agent_id, 
    client_id, 
    view_counts, 
    is_sold
)
SELECT 
  'Property ' || x, 
  100000 + (x * 1000), 
  'Address ' || x, 
  500 + (x * 10), 
  CASE 
    WHEN x % 3 = 1 THEN 'low'
    WHEN x % 3 = 2 THEN 'medium'
    ELSE 'high'
  END, 
  CASE 
    WHEN x % 4 = 1 THEN 'hdb'
    WHEN x % 4 = 2 THEN 'condo'
    WHEN x % 4 = 3 THEN 'apartment'
    ELSE 'studio'
  END, 
  CASE 
    WHEN x % 3 = 1 THEN 'partially_furnished'
    WHEN x % 3 = 2 THEN 'fully_furnished'
    ELSE 'not_furnished'
  END, 
  2000 + (x % 21), 
  CURRENT_TIMESTAMP, 
  (SELECT id FROM user WHERE userid = 'user4'), 
  'user3', 
  0, 
  FALSE
FROM cnt;



/* 100 Reviews */
WITH RECURSIVE
  cnt(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM cnt WHERE x < 100)
INSERT INTO review (
    author_userid, 
    agent_id, 
    create_date, 
    rating, 
    content
)
SELECT 
  CASE 
    WHEN x % 2 = 1 THEN 'user2'
    ELSE 'user3'
  END, 
  CASE 
    WHEN x % 2 = 1 THEN (SELECT id FROM user WHERE userid = 'user4')
    ELSE (SELECT id FROM user WHERE userid = 'user7')
  END,
  CURRENT_TIMESTAMP,
  (x % 5) + 1,
  'Review content ' || x
FROM cnt;