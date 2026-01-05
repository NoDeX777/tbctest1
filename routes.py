from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from ext import db
from modules import User, Product, Category, Cart, CartItem

def init_routes(app):

    @app.route("/")
    def home():
        products = Product.query.filter_by(approved=True).limit(6).all()
        return render_template("home.html", products=products)

    @app.route("/products")
    def products():
        products = Product.query.filter_by(approved=True).all()
        return render_template("products.html", products=products)

    @app.route("/product/<int:id>")
    def product_detail(id):
        product = Product.query.get_or_404(id)
        if not product.approved and product.user_id != getattr(current_user, "id", None):
            return redirect("/")
        return render_template("product_detail.html", product=product)

    @app.route("/register", methods=["GET","POST"])
    def register():
        if request.method == "POST":
            user = User(
                username=request.form["username"],
                email=request.form["email"],
                password=request.form["password"]
            )
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        return render_template("register.html")

    @app.route("/login", methods=["GET","POST"])
    def login():
        if request.method == "POST":
            user = User.query.filter_by(username=request.form["username"]).first()
            if user and user.password == request.form["password"]:
                login_user(user)
                return redirect("/")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect("/")

    @app.route("/product/add", methods=["GET","POST"])
    @login_required
    def add_product():
        categories = Category.query.all()
        if request.method == "POST":
            product = Product(
                title=request.form["title"],
                description=request.form["description"],
                price=request.form["price"],
                category_id=request.form["category"],
                user_id=current_user.id
            )
            db.session.add(product)
            db.session.commit()
            return redirect("/my-products")
        return render_template("add_product.html", categories=categories)

    @app.route("/my-products")
    @login_required
    def my_products():
        products = Product.query.filter_by(user_id=current_user.id).all()
        return render_template("my_products.html", products=products)

    @app.route("/admin")
    @login_required
    def admin():
        if current_user.role != "admin":
            return redirect("/")
        products = Product.query.filter_by(approved=False).all()
        return render_template("admin.html", products=products)

    @app.route("/approve/<int:id>")
    @login_required
    def approve(id):
        if current_user.role == "admin":
            product = Product.query.get(id)
            product.approved = True
            db.session.commit()
        return redirect("/admin")
