from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import openai
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Continuing with system environment variables...")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Configure CORS to allow credentials and specific origins
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Secret key for JWT
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')  # Use environment variable
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID', '67683186421-8vjvf0k4sho43htao5uvnr3jyrteqo.apps.googleusercontent.com')

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENROUTER_API_KEY")  # Use OpenRouter API key
openai.api_base = "https://openrouter.ai/api/v1"  # OpenRouter API base URL

# Load MongoDB URI from environment
MONGODB_URI = os.getenv('MONGODB_URI')
print('MONGODB_URI:', MONGODB_URI)  # Debug output
if not MONGODB_URI or not MONGODB_URI.startswith('mongodb+srv://'):
    raise Exception('MONGODB_URI is not set correctly in your .env file!')
client = MongoClient(MONGODB_URI)
# Use the correct database name from your URI/app: 'login-credentials'
db = client['login-credentials']
users_collection = db['users']

# Simple responses for demonstration
RESPONSES = {
    "hello": "Hi there! How can I help you?",
    "how are you": "I'm doing well, thank you for asking!",
    "bye": "Goodbye! Have a great day!",
    "what is your name": "I'm ChatBot, nice to meet you!",
    "help": "I can respond to basic greetings and questions. Try saying 'hello' or asking 'how are you'!",
    "default": "I'm not sure how to respond to that. Could you please rephrase?"
}

def generate_unique_username(email):
    """Generates a unique username from an email address."""
    username = email.split('@')[0].lower().replace('.', '')
    if username not in users_collection.find_one({'username': username}):
        return username
    
    counter = 1
    while True:
        new_username = f"{username}{counter}"
        if new_username not in users_collection.find_one({'username': new_username}):
            return new_username
        counter += 1

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        logger.info(f"Received Authorization header: {token}")
        
        if not token:
            logger.error("Token is missing")
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            logger.info(f"Extracted token: {token[:20]}...")
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            logger.info(f"Decoded token data: {data}")
            
            current_user = users_collection.find_one({'username': data['username']})
            logger.info(f"Found user in DB: {current_user is not None}")
            
            if not current_user:
                logger.error(f"User {data['username']} not found in users_collection")
                return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route("/")
def home():
    return jsonify({"status": "Chatbot API is running!"})

@app.route("/api/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    if '@' in username:
        return jsonify({'error': 'Username cannot contain the "@" symbol.'}), 400

    if users_collection.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({
        'username': username,
        'password': hashed_password,
        'role': 'user'
    })
    return jsonify({'message': 'User registered successfully'}), 201

@app.route("/api/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password')

    logger.info(f"Login attempt for username: '{username}'")
    user = users_collection.find_one({'username': username})

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        logger.error(f"Invalid credentials for user: {username}")
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({
        'username': username,
        'role': user['role'],
        'exp': int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp())
    }, app.config['SECRET_KEY'])
    
    logger.info(f"Generated token for user {username}")
    
    return jsonify({
        'token': token,
        'username': username,
        'role': user['role']
    })

@app.route("/api/login/google", methods=['POST'])
def google_login():
    data = request.get_json()
    token = data.get('token')
    
    if not token:
        return jsonify({'error': 'Google token is missing'}), 400

    try:
        id_info = id_token.verify_oauth2_token(
            token, google_requests.Request(), app.config['GOOGLE_CLIENT_ID']
        )
        
        google_sub = id_info['sub']
        email = id_info.get('email')
        
        # Find user by google_sub
        found_user = None
        username = None
        for u_name, u_data in users_collection.find():
            if u_data.get("google_sub") == google_sub:
                found_user = u_data
                username = u_name
                break

        if not found_user:
            # If not found, create a new user
            new_username = generate_unique_username(email)
            users_collection.insert_one({
                'username': new_username,
                'password': None, # No password for Google users
                'role': 'user',
                'google_sub': google_sub,
                'email': email,
                'name': id_info.get('name')
            })
            username = new_username
            found_user = users_collection.find_one({'username': username})
            logger.info(f"New user created via Google: {username}")
        else:
            logger.info(f"User found via Google: {username}")
        
        # Generate our app's JWT token
        app_token = jwt.encode({
            'username': username,
            'role': found_user['role'],
            'exp': int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp())
        }, app.config['SECRET_KEY'])

        return jsonify({
            'token': app_token,
            'username': username,
            'role': found_user['role']
        })

    except ValueError as e:
        # Invalid token
        logger.error(f"Google token validation error: {str(e)}")
        return jsonify({'error': 'Invalid Google token'}), 401
    except Exception as e:
        logger.error(f"Error during Google login: {str(e)}")
        return jsonify({'error': 'An internal error occurred'}), 500

@app.route("/api/chat", methods=['POST'])
@token_required
def chat(current_user):
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip().lower()
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Try OpenAI API first
        try:
            response = openai.ChatCompletion.create(
                model="anthropic/claude-3.5-sonnet",  # Use OpenRouter model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_reply = response['choices'][0]['message']['content']
            return jsonify({'response': bot_reply})
        except Exception as openai_error:
            # Fallback to old RESPONSES if OpenAI fails
            response = RESPONSES.get(user_message, RESPONSES["default"])
            return jsonify({'response': response, 'note': 'OpenRouter fallback: ' + str(openai_error)})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/api/admin/users", methods=['GET'])
@token_required
def get_users(current_user):
    if current_user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    users = [{'username': username, 'role': data['role']} 
             for username, data in users_collection.find()]
    return jsonify({'users': users})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)