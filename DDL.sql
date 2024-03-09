CREATE TABLE zipcode (
  zipcode_id INT PRIMARY KEY,
  avg_income INT NOT NULL,
  population INT NOT NULL
);

-- merges the Is in A relation with Business
CREATE TABLE Business (
    business_id INT PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(255),
    zipcode INT,
    address VARCHAR(255),
    review_count INT,
    state VARCHAR(255),
    average_rating DECIMAL,
    total_checkins INT,
    stars DECIMAL,
    FOREIGN KEY (zipcode) REFERENCES Zipcode(zipcode_id)
);

-- merged the Is Given relation with Reviews
CREATE TABLE Review (
    review_id INT PRIMARY KEY,
    stars DECIMAL,
    business_id INT,
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE Categories (
    name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Has (
    business_id INT,
    category_id INT,
    PRIMARY KEY (business_id, name),
    FOREIGN KEY (business_id) REFERENCES Business(business_id),
    FOREIGN KEY (name) REFERENCES Categories(name)
);

-- merged the Gets relation with Checkins
CREATE TABLE Check_ins (
    business_id INT,
    day DATE,
    count INT,
    PRIMARY KEY (business_id, day),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);