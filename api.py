from flask import Flask  # Import Flask for web framework
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database interaction
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort  # Import RESTful API tools

# Create a Flask app instance
app = Flask(__name__)

# Configure the SQLite database URI. (database.db will be created in the current directory)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize SQLAlchemy and Flask-RESTful API
db = SQLAlchemy(app)
api = Api(app)

# Define the User database model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique, non-null username

    def __repr__(self):
        return f"User(username={self.username})"  # String representation for debugging

# Define request arguments for user creation and update
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username is required')

# Define fields to marshal user data for API responses
user_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
}

# Resource for handling multiple users (GET, POST)
class UserListResource(Resource):
    @marshal_with(user_fields)  # Marshal response data using user_fields
    def get(self):
        all_users = User.query.all()  # Retrieve all users from the database
        return all_users, 200 #return the users, and a 200 ok code.

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()  # Parse request arguments
        new_user = User(username=args['username'])  # Create a new User object
        db.session.add(new_user)  # Add the user to the database session
        db.session.commit()  # Commit the changes to the database
        return new_user, 201  # Return the created user and 201 Created status

# Resource for handling a single user (GET, PATCH, DELETE)
class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()  # Retrieve the user by ID
        if not user:
            abort(404, "User not found")  # Abort with 404 if user doesn't exist
        return user, 200

    @marshal_with(user_fields)
    def patch(self, user_id):
        args = user_parser.parse_args()  # Parse request arguments
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, "User not found")
        user.username = args["username"]  # Update the user's username
        db.session.commit()  # Commit the changes
        return user, 200

    @marshal_with(user_fields)
    def delete(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)  # Delete the user
        db.session.commit()  # Commit the deletion
        return '', 204 #Returns a 204 no content, as the data is deleted.

# Add resources to the API
api.add_resource(UserListResource, '/api/users')  # Endpoint for user list
api.add_resource(UserResource, '/api/users/<int:user_id>')  # Endpoint for single user

# Simple root route
@app.route('/')
def home():
    return '<h1>Flask User API</h1>'

# Run the app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)