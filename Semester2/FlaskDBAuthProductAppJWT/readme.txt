--To Run the application:

--create a virtual environment inside the project folder

python -m venv env

--activate that virtual environment

env\Scripts\activate

--install the dependencies inside the activated virtual environment

pip install -r requirements.txt

--run the application:

python app.py

--On first run, an admin user will automatically be created:
- Email: admin@gmail.com
- Password: admin123



--To test the following endpoints use the Postman software or any HTTP client tool


API Endpoints:
--------------
- `POST /registerapi` – Register a new user via JSON
- `POST /loginapi` – Login and receive JWT token
- `GET /products` – Get all products (JWT required)
- `POST /products` – Add a new product (JWT required)
- `GET /products/<productid>` – Get single product (JWT required)
- `PUT /products/<productid>` – Update product (JWT required)
- `DELETE /products/<productid>` – Delete product (Admin role only, JWT required)
- `GET /products/category/<category>` – Filter products by category (JWT required)


List of Sample payload of different functionalities:
-----------------------------------------------------

1. User Registration Endpoint

POST /registerapi

{
  "name": "John Doe",
  "email": "john@example.com",
  "mobile": "9876543210",
  "password": "john123",
  "role": "user"     // Optional: "user" or "admin"
}


2. User Login Endpoint

POST /loginapi

{
  "username": "john@example.com",
  "password": "john123"
}


Response will contain JWT token like:

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}


Use this token as Bearer in headers for the protected endpoints:

Authorization: Bearer <access_token>



PRODUCT ENDPOINTS (JWT Required)
=================================

3. Add New Product

POST /products


{
  "name": "Laptop",
  "price": "70000",
  "quantity": 5,
  "category": "Electronics"
}


4. Update Existing Product

PUT /products/<productid>

{
  "name": "Gaming Laptop",
  "price": "85000",
  "quantity": 3,
  "category": "Electronics"
}


5. Get Product By ID

GET /products/<productid>

No body required.


6. Delete Product

DELETE /products/<productid>

Requires JWT Token of admin role.

No body required.


7. Get All Products

GET /products

No body required.


8. Get Products by Category
GET /products/category/<category>

Example:
/products/category/Electronics

No body required.


