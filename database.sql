CREATE DATABASE YashDB;
CREATE TABLE Customers (
CustomerID INT,
CustomerName VARCHAR(50),
City VARCHAR(30),
JoinDate DATE
);
INSERT INTO Customers VALUES
(101, 'Rahul Sharma', 'Bangalore', '2023-01-15'),
(102, 'Priya Mehta', 'Mumbai', '2024-03-20'),
(103, 'Arjun Nair', 'Chennai', '2025-01-12'),
(104, 'Sneha Gupta', 'Delhi', '2022-07-10'),
(105, 'Kavya Reddy', 'Hyderabad', '2024-08-15'),
(106, 'Amit Verma', 'Pune', '2023-11-05'),
(107, 'Rohan Singh', 'Kolkata', '2024-05-18'),
(108, 'Simran Kaur', 'Delhi', '2025-02-01'),
(109, 'Anjali Jain', 'Mumbai', '2023-09-22'),
(110, 'Vikram Patel', 'Ahmedabad', '2022-12-30');

CREATE TABLE ORDERS (
OrderID INT,
CustomerID INT,
OrderDate DATE,
OrderAmount DECIMAL(10,2),
Status VARCHAR(20)
);

INSERT INTO Orders VALUES
(5001,101,'2025-01-05',12000,'Delivered'),
(5002,102,'2025-01-15',8500,'Pending'),
(5003,101,'2025-02-10',22000,'Delivered'),
(5004,104,'2025-02-15',4500,'Cancelled'),
(5005,103,'2025-03-01',17500,'Delivered'),
(5006,105,'2025-03-10',9800,'Pending'),
(5007,106,'2025-03-18',25000,'Delivered'),
(5008,107,'2025-04-02',14500,'Delivered'),
(5009,101,'2025-04-10',30000,'Delivered'),
(5010,109,'2025-04-15',6500,'Pending'),
(5011,110,'2025-05-01',42000,'Delivered'),
(5012,104,'2025-05-08',18000,'Delivered'),
(5013,106,'2025-05-15',7000,'Cancelled'),
(5014,102,'2025-05-20',27000,'Delivered'),
(5015,107,'2025-06-01',15500,'Pending');

CREATE TABLE Employees (
EmployeeID INT,
EmployeeName VARCHAR(50),
ManagerID INT,
Department VARCHAR(30),
JoiningDate DATE,
Salary DECIMAL(10,2)
);

INSERT INTO Employees VALUES
(1,'Rajesh Kumar',NULL,'Management','2018-01-10',150000),
(2,'Neha Sharma',1,'Sales','2020-03-15',90000),
(3,'Amit Gupta',1,'IT','2019-06-20',110000),
(4,'Priyanka Singh',2,'Sales','2022-01-12',65000),
(5,'Vikas Patel',2,'Sales','2021-09-18',70000),
(6,'Rohit Jain',3,'IT','2023-02-05',60000),
(7,'Anjali Verma',3,'IT','2022-11-10',62000),
(8,'Karan Mehta',1,'HR','2021-05-25',80000),
(9,'Sneha Kapoor',8,'HR','2024-01-05',50000),
(10,'Arjun Malhotra',3,'IT','2024-04-15',55000);

-- Question 1
SELECT 
    o.OrderID,
    c.CustomerName,
    o.OrderAmount
FROM Orders o
JOIN Customers c
    ON o.CustomerID = c.CustomerID
ORDER BY o.OrderAmount DESC
LIMIT 5;

-- Question 2: Customers whose names start with A, R, or S
SELECT *
FROM Customers
WHERE CustomerName REGEXP '^[ARS]';

-- Question 3: Pending orders worth more than ₹10,000
SELECT 
    c.CustomerName,
    o.OrderID,
    o.OrderAmount,
    o.Status
FROM Customers c
JOIN Orders o
    ON c.CustomerID = o.CustomerID
WHERE o.OrderAmount > 10000
  AND o.Status = 'Pending';
  
  -- Question 4: Display the joining date
  SELECT 
    customer_id,
    DATEDIFF(CURDATE(), joining_date) AS days_associated
FROM customers
WHERE DATEDIFF(CURDATE(), joining_date) > 365;

-- Question 5
-- Total Amount After GST, and Expected Collection Date (15 days after order date).

SELECT
    order_id AS "Order ID",
    amount AS "Current Amount",
    amount * 0.18 AS "18% GST",
    amount + (amount * 0.18) AS "Total Amount After GST",
    DATE_ADD(order_date, INTERVAL 15 DAY) AS "Expected Collection Date"
FROM orders;

-- Question 6
-- The operations team wants to review the customers ranked between 11th and 20th highest orders.

SELECT
    customer_id,
    customer_name,
    total_orders
FROM customers
ORDER BY total_orders DESC
LIMIT 10 OFFSET 10;

-- Question 7
-- Display Customer ID, Customer Name, Join Date, and Number of Days Since Registration.

SELECT
    c.customer_id AS "Customer ID",
    c.customer_name AS "Customer Name",
    c.join_date AS "Join Date",
    DATEDIFF(CURDATE(), c.join_date) AS "Number of Days Since Registration"
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;

-- Question 8
-- Using a JOIN, display Employee Name, Manager Name, and Department.

SELECT
    e.employee_name AS "Employee Name",
    m.employee_name AS "Manager Name",
    e.department AS "Department"
FROM employees e
JOIN employees m
    ON e.manager_id = m.employee_id;
    
-- Question 9
-- Display Customer Name, Join Date, Order Date, and Days Taken To Place First Order.

SELECT
    c.customer_name AS "Customer Name",
    c.join_date AS "Join Date",
    o.order_date AS "Order Date",
    DATEDIFF(o.order_date, c.join_date) AS "Days Taken To Place First Order"
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE DATEDIFF(o.order_date, c.join_date) <= 30;

-- Question 10
-- Customer Name, Total Purchase Amount,
-- Spending Category, and Loyalty Status.

SELECT
    c.customer_name AS "Customer Name",
    SUM(o.amount) AS "Total Purchase Amount",
    CASE
        WHEN SUM(o.amount) > 50000 THEN 'Premium'
        WHEN SUM(o.amount) >= 20000 THEN 'Gold'
        ELSE 'Silver'
    END AS "Spending Category",
    CASE
        WHEN c.join_date < '2024-01-01' THEN 'Loyal Customer'
        ELSE 'New Customer'
    END AS "Loyalty Status"
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.join_date;

/* Question 11
An online marketplace wants to find customers whose order amount
is higher than the average order amount of all orders.
Display Customer Name, Order ID, and Order Amount. */

SELECT
    c.customer_name AS "Customer Name",
    o.order_id AS "Order ID",
    o.amount AS "Order Amount"
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.amount > (
    SELECT AVG(amount)
    FROM orders
);

-- Question 12
-- The management team wants the 2nd to 6th highest orders placed by customers.

SELECT
    c.customer_name AS "Customer Name",
    o.order_id AS "Order ID",
    o.amount AS "Order Amount"
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY o.amount DESC
LIMIT 5 OFFSET 1;

