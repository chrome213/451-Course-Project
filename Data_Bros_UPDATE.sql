-- Updates the buisness table with the number of check-ins for each business
UPDATE Business 
SET numCheckins = (SELECT SUM(count) 
FROM Check_ins 
WHERE Check_ins.business_id = Business.business_id);

-- Updates the business table with the number of reviews for each business
UPDATE Business 
SET review_count = (SELECT COUNT(*) 
FROM Review 
WHERE Review.business_id = Business.business_id);

-- Updates the business table with the average rating for each business
UPDATE Business 
SET reviewRating = (SELECT AVG(stars) 
FROM Review 
WHERE Review.business_id = Business.business_id);