from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.exceptions import HTTPException

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite database file
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy modification tracking

# Initialize database and other extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    notes = db.relationship('Notes', backref='user', lazy=True)

# Notes Model
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# User loader for login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create all database tables if they don't exist
def create_tables():
    """Creates tables in the database if they don't already exist."""
    with app.app_context():
        db.create_all()  # Automatically creates tables based on models if not already created

# Routes
@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check for user in database
        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            flash("Invalid username or password", "danger")
            return redirect("/login")

        login_user(user)
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    logout_user()
    return redirect("/")

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if the username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists. Please choose another one.", "danger")
            return redirect("/register")

        # Create new user and save to the database
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! You can now log in.", "success")
        return redirect("/login")

    return render_template("register.html")

# Handle errors gracefully
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Custom error handler"""
    flash(f"An error occurred: {e.description}", "danger")
    return redirect(url_for("home"))

# Run the application
if __name__ == '__main__':
    create_tables()  # Ensure tables are created before the app starts
    app.run(debug=True)
