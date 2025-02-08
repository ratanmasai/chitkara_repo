from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from functools import wraps


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

app.config["SECRET_KEY"] = "Your secret key"


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


class User(db.Model, UserMixin):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Product(db.Model):

    __tablename__ = "product"

    productid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(100))

    def __repr__(self):
        return f"ProductId: {self.productid} Name: {self.name} Price: {self.price} Quantity: {self.quantity} Category: {self.category}"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()

    # Check if an admin user already exists
    if not User.query.filter_by(role="admin").first():
        admin_user = User(name="Admin", email="admin@gmail.com",
                          mobile="1234567890", role="admin")
        admin_user.set_password("admin123")  # Set a default password
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with email: admin@gmail.com and password: admin123")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        user = User.query.filter_by(email=email, role=role).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        mobile = request.form.get("mobile")

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        # Check if the email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        new_user = User(name=name, email=email, mobile=mobile)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("/register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash("Access denied!", "danger")
            return redirect(url_for('dashboard'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/admin')
@login_required
@admin_required
def admin():
    return "Welcome to the admin panel!"


@app.route("/product", methods=["GET", "POST"])
@login_required
def product():

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        category = request.form.get("category")

        product = Product(name=name, price=price,
                          quantity=quantity, category=category)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("product"))

    products = Product.query.all()
    return render_template("product.html", products=products)


@app.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):
    product = db.session.get(Product, id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("product"))


@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    product = db.session.get(Product, id)
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        category = request.form.get("category")

        product.name = name
        product.price = price
        product.quantity = quantity
        product.category = category

        db.session.add(product)
        db.session.commit()
        return redirect(url_for("product"))

    return render_template("update_product.html", product=product)


if __name__ == "__main__":
    app.run(debug=True)
