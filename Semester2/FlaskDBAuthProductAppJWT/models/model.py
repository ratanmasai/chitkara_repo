
from . import db
from flask_login import UserMixin
from flask_bcrypt import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "mobile": self.mobile,
            "role": self.role
        }


class Product(db.Model):

    __tablename__ = "product"

    productid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(100))

    def __repr__(self):
        return f"ProductId: {self.productid} Name: {self.name} Price: {self.price} Quantity: {self.quantity} Category: {self.category}"

    def as_dict(self):
        return {
            "productid": self.productid,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }
