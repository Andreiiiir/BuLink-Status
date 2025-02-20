from app import db  # Import the database instance
from app.auth.models import User  # Import the User model
from app import create_app  # Import your Flask app factory

def create_user(username, password):
    app = create_app()  # Create the Flask app context
    with app.app_context():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Error: User with username '{username}' already exists.")
            return

        # Create a new user and set the password
        user = User(username=username)
        user.set_password(password)  # Hash and set the password

        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        print(f"User '{username}' has been created successfully.")

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_user(username, password)
