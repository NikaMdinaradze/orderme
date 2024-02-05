CREATE TABLE owner(
    owner_id SERIAL PRIMARY KEY,
    username VARCHAR(24) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20),
    picture_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE restaurant (
    restaurant_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(255),
    is_active BOOLEAN,
    logo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES owner(owner_id)
);
CREATE TABLE photo(
    photo_id SERIAL PRIMARY KEY,
    url VARCHAR(255),
    restaurant_id INT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
);
