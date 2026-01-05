from flask import Flask
from ext import db, login_manager
from routes import init_routes
from modules import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

init_routes(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)