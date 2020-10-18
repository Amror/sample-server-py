import pymongo
import json
import hashlib
from datetime import datetime
from os import urandom
from re import match
from user import User

with open('db_config.json', 'r') as f:
    # Get db username, pass and address from
    db_config = json.loads(f.read())

DB_USERNAME = db_config['USERNAME']
DB_PASSWORD = db_config['PASSWORD']
DB_ADDRESS = db_config['ADDRESS']

recipe_names = ['Cake', 'Brownies', 'Hot Chocolate', 'Chocolate Pudding', 'Molten Cake']

client = pymongo.MongoClient(f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_ADDRESS}/')

# Access website database
database = client['website']

# Access users collection
users = database['users']

def create_user(email: str, username: str, password: str) -> User:
    """Creates a user uploads user data into database
    then return a user object with matching data"""

    # Validate data with regex rules
    if match(r'[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,63}$', email) and match(r'\w{2,10}$', username) and match(r'[\w\*\+\!\&]{8,20}$', password):
        # 1 account per email
        if users.find_one({'email': email}):
            return
        # Create a 16 bytes salt
        salt = urandom(16)
        hashed_password = hashlib.sha256(bytes(password, 'utf-8') + salt).digest()
        creation_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        ratings = {name: 0 for name in recipe_names}

        # Insert new user data
        users.insert_one({
            'username': username,
            'email': email,
            'hashed_password': hashed_password,
            'salt': salt,
            'creation_date': creation_date,
            'ratings': ratings
        })

        return User(username, email, creation_date, ratings)

    # else:
    #    raise ValueError('Data doesnt match regex rules')

def get_user(email: str, password: str) -> User:
    """Get a user by email and password if the user exists"""
    
    user_data = users.find_one({'email': email})
    if user_data:
        salt = user_data['salt']
        hashed_password = user_data['hashed_password']
        received_password = hashlib.sha256(bytes(password, 'utf-8') + salt).digest()
        # Checked if received password is the same as the one stored in the document
        if hashed_password != received_password:
            return

        return User(user_data['username'], user_data['email'], user_data['creation_date'], user_data['ratings'])


def update_user(email, key, value):
    """Updates user info in the database based on given key value"""

    if key == 'password' and match(r'[\w\*\+\!\&]{8,20}$', value):
        # Regenerate salt and update password + salt
        salt = urandom(16)
        result = users.update_one({'email': email},
                        {'$set': {'hashed_password': hashlib.sha256(bytes(value, 'utf-8') + salt).digest(),
                        'salt': salt}})
        return result.modified_count
    
    elif key == 'email' and match(r'[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,63}$', value):
        result = users.update_one({'email': email},
                                 {'$set': {'email': value}})
        return result.modified_count
    
    elif key == 'username' and match(r'\w{2,10}$', value):
        result = users.update_one({'email': email},
                                 {'$set': {'username': value}})
        return result.modified_count
    
    elif key == 'rating' and type(value) is tuple and value[0] in recipe_names and 0 <= value[1] <= 5:
        result = users.update_one({'email': email},
                                {'$set': {f'ratings.{value[0]}': value[1]}})
        return result.modified_count

    # Nothing affected
    return 0


def delete_user(email):
    """Deletes user by email from db by their email"""
    result = users.delete_one({'email': email})
    return result.deleted_count