import requests
import json  # For working with JSON data

base_url = "http://127.0.0.1:5000/api/users"  # Base URL for the API

# Example data for POST and PUT requests
user_data = {"username": "Hello"}

# Function to handle GET requests
def get_user(user_id=None):
    """Retrieves user data. If user_id is provided, retrieves a single user; otherwise, retrieves all users."""
    url = f"{base_url}/{user_id}" if user_id else base_url  # Construct URL based on user_id
    response = requests.get(url)  # Send GET request

    if response.status_code == 200:  # Check for successful response
        print("GET successful:", response.json())  # Print the JSON response
        return response.json()
    else:
        print(f"GET error: {response.status_code}, {response.text}") #print the error code and text.
        return None

# Function to handle POST requests (create a new user)
def create_user(data):
    """Creates a new user with the provided data."""
    response = requests.post(base_url, json=data)  # Send POST request with JSON data

    if response.status_code == 201:  # Check for successful creation (201 Created)
        print("User created:", response.json())
        return response.json()
    else:
        print(f"POST error: {response.status_code}, {response.text}")
        return None

# Function to handle PUT/PATCH requests (update an existing user)
def update_user(user_id, data):
    """Updates an existing user with the provided data."""
    url = f"{base_url}/{user_id}"
    response = requests.patch(url, json=data)  # Send PATCH request with JSON data. You can also use PUT.

    if response.status_code == 200:  # Check for successful update
        print("User updated:", response.json())
        return response.json()
    else:
        print(f"PUT/PATCH error: {response.status_code}, {response.text}")
        return None

# Function to handle DELETE requests
def delete_user(user_id):
    """Deletes a user with the specified ID."""
    url = f"{base_url}/{user_id}"
    response = requests.delete(url)  # Send DELETE request

    if response.status_code == 204:  # Check for successful deletion (204 No Content)
        print("User deleted successfully")
        return True
    elif response.status_code == 200:
        print("user deleted successfully")
        return True
    else:
        print(f"DELETE error: {response.status_code}, {response.text}")
        return False

# Example usage:
print("--- GET all users ---")
get_user()

print("\n--- GET user with ID 1 ---")
get_user(1)

print("\n--- POST (create) a user ---")
create_user(user_data)

# print("\n--- PUT/PATCH (update) user with ID 2 ---")
# update_user(2, {"username": "Dasepalli"})
#
# print("\n--- DELETE user with ID 3 ---")
# delete_user(1)
#
# print("\n--- GET all users after changes ---")
# get_user()