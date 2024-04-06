CREATE TABLE zipcode (
  zipcode_id INT PRIMARY KEY,
  avg_income INT NOT NULL,
  population INT NOT NULL
);

-- merges the Is in A relation with Business
CREATE TABLE Business (
    business_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(50),
    zipcode INT,
    address VARCHAR(255),
    review_count INT,
    state VARCHAR(3),
    average_rating DECIMAL,
    total_checkins INT,
    stars DECIMAL,
    FOREIGN KEY (zipcode) REFERENCES Zipcode(zipcode_id)
);

-- merged the Is Given relation with Reviews
CREATE TABLE Review (
    review_id VARCHAR(255) PRIMARY KEY,
    stars DECIMAL,
    business_id VARCHAR(255),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE Categories (
    name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE Has (
    business_id VARCHAR(255),
    category_id VARCHAR(255),
    PRIMARY KEY (business_id, name),
    FOREIGN KEY (business_id) REFERENCES Business(business_id),
    FOREIGN KEY (name) REFERENCES Categories(name)
);

-- merged the Gets relation with Checkins
CREATE TABLE Check_ins (
    business_id VARCHAR(255),
    day VARCHAR(10),
    count INT,
    PRIMARY KEY (business_id, day),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);