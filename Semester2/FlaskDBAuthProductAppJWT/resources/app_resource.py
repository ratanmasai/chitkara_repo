from flask import Flask, request
from flask_restful import Api, Resource
from models import db

from models.model import User
from models.model import Product

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


jwt = JWTManager()


class UserRegisterResource(Resource):
    def post(self):
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        mobile = data.get("mobile")
        password = data.get("password")
        role = data.get("role", "user")

        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists."}, 400
        user = User(name=name, email=email,
                    mobile=mobile, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully."}, 201


# User Login Resource


class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(email=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(
                identity=user.role)

            return {"access_token": access_token}, 200

        return {"message": "Invalid credentials."}, 401


# Product Resource


class ProductResource(Resource):
    @jwt_required()
    def get(self, productid):
        product = db.session.get(Product, productid)

        if product:
            return product.as_dict()
        else:
            return {"message": "Product Not Found!"}, 404

    @jwt_required()
    def post(self):
        data = request.get_json()

        name = data.get("name")
        price = data.get("price")
        quantity = data.get("quantity")
        category = data.get("category")

        if not all([name, price, quantity, category]):
            return {"message": "All fields (name, price, quantity, category) are required."}, 400

        new_product = Product(name=name, price=price,
                              quantity=quantity, category=category)
        db.session.add(new_product)
        db.session.commit()
        return {"message": "Product Added Successfully", "product": new_product.as_dict()}, 201

    @jwt_required()
    def put(self, productid):
        product = db.session.get(Product, productid)
        if product:
            data = request.get_json()
            product.name = data.get("name", product.name)
            product.price = data.get("price", product.price)
            product.quantity = data.get("quantity", product.quantity)
            product.category = data.get("category", product.category)

            db.session.add(product)
            db.session.commit()
            return {"message": "Product Updated Successfully", "Product": product.as_dict()}, 200
        else:
            return {"message": "Product Not Found!"}, 404

    @jwt_required()
    def delete(self, productid):
        identity = get_jwt_identity()
        print(identity)
        if identity != "admin":
            return {"message": "Unauthorized: Admins only."}, 403
        product = db.session.get(Product, productid)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product deleted successfully", "product": product.as_dict()}
        return {"message": "Product Not Found!"}, 404


# Products Resource


class ProductsResource(Resource):
    @jwt_required()
    def get(self):
        # Get all products
        allproducts = Product.query.all()

        # Converting them to the list of json
        # products = [ product.as_dict() for product in allproducts]
        products = []
        for product in allproducts:
            products.append(product.as_dict())

        if products:
            return {"products": products}
        else:
            return {"message": "No Products Available!"}


class ProductCategory(Resource):
    @jwt_required()
    def get(self, category):

        allproducts = Product.query.filter_by(
            category=category).all()

        # Converting it to the JSON
        # category_products = [product.as_dict() for product in all_category_products]
        products = []
        for product in allproducts:
            products.append(product.as_dict())

        if products:
            return {"products": products}
        else:
            return {"message": "No products found in this category"}, 404
