# Python-React Chatbot

A simple chatbot application with a Python Flask backend and React frontend, powered by OpenRouter AI.

## Project Structure
```
chatbot/
├── app.py                 # Main Flask backend
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this file)
├── backend/
│   ├── package.json
│   └── package-lock.json
└── frontend/
    ├── package.json
    └── src/
        └── App.js
```

## Setup Instructions

### Environment Variables Setup
1. Create a `.env` file in the root directory with the following variables:
   ```
   # OpenRouter API Configuration
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   
   # Flask Configuration
   FLASK_SECRET_KEY=your-secret-key-here
   
   # Google OAuth Configuration (optional)
   GOOGLE_CLIENT_ID=your_google_client_id_here
   ```

2. Get your OpenRouter API key:
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Navigate to your API keys section
   - Copy your API key and paste it in the `.env` file

### Backend Setup
1. Navigate to the project root directory:
   ```
   cd chatbot
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the Flask server:
   ```
   python app.py
   ```
   The backend will run on http://localhost:5000

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   The frontend will run on http://localhost:3000

## Usage
1. Open your browser and go to http://localhost:3000
2. Register or login to your account
3. Type your message in the input field and press Enter or click Send
4. The chatbot will respond using OpenRouter's AI models

## Features
- Real-time chat interface with AI-powered responses
- User authentication and registration
- Google OAuth integration
- Material-UI components for a modern look
- OpenRouter AI integration for intelligent responses
- Cross-Origin Resource Sharing (CORS) enabled
- Fallback response system if AI is unavailable 