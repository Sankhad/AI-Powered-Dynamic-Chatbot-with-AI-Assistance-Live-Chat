
# 🤖 Python-React Chatbot — AI-Powered with OpenRouter & JWT

A dynamic full-stack chatbot application combining **React.js frontend** and **Python Flask backend**, integrated with **OpenRouter AI**, **MongoDB**, and **JWT-based authentication**.

> 💬 Developed by a collaborative team of passionate developers from Sister Nivedita University, ST. Xavier’s, and GNIT.

---

## 📁 Project Structure

```

chatbot/
├── app.py                 # Main Flask backend
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this file)
├── backend/
│   ├── package.json
│   └── package-lock.json
└── frontend/
├── package.json
└── src/
└── App.js

```

---

## 🧪 Setup Instructions

### 🔐 Environment Variables Setup

Create a `.env` file in the root directory with:

```

# OpenRouter API Configuration

OPENROUTER\_API\_KEY=your\_openrouter\_api\_key\_here

# Flask Configuration

FLASK\_SECRET\_KEY=your-secret-key-here

# Google OAuth Configuration (optional)

GOOGLE\_CLIENT\_ID=your\_google\_client\_id\_here

# MongoDB Connection String

MONGO\_URI=your\_mongo\_db\_connection\_here

````

---

### ⚙️ Backend Setup

```bash
cd chatbot
python -m venv venv
venv\Scripts\activate      # Or use: source venv/bin/activate
pip install -r requirements.txt
python app.py              # Starts backend at http://localhost:5000
````

---

### 💻 Frontend Setup

```bash
cd frontend
npm install
npm start                  # Opens at http://localhost:3000
```

---

## 🚀 Usage Guide

1. Go to [http://localhost:3000](http://localhost:3000)
2. Register or log in using your credentials or Google account
3. Type messages — the chatbot replies using OpenRouter AI (Claude, GPT, etc.)
4. Admin users can view registered users
5. All chat messages and user data are saved via MongoDB

---

## 🌟 Key Features

* 🔐 **JWT Authentication** + Google OAuth
* 🤖 **AI Responses** via OpenRouter API (Claude 3.5 / GPT)
* 🗃️ **MongoDB Integration** for storing chat and user data
* 🧠 **Fallback System** for handling unclear inputs
* 📱 **Responsive React Frontend**
* 🛡️ **Environment Protected API Keys**
* 🎨 **Modern UI** with clean layout
* 📄 **Admin Panel** for managing users

---

## 👨‍💻 Team Members & Responsibilities

| 👤 Name                                | 🎓 Institution                     | 💼 Role & Responsibility                            |
| -------------------------------------- | ---------------------------------- | --------------------------------------------------- |
| **Sankhadip Maji** *(Team Lead)*       | Sister Nivedita University         | 🧠 Backend Developer – Flask API, JWT, AI Logic     |
| **Soumangi Chakraborty** *(Vice Lead)* | Sister Nivedita University         | 🎨 Frontend Developer – React UI & chat design      |
| **Ekarna Chakraborty** *(Member)*      | Guru Nanak Institute of Technology | 🏗️ Architect – Project architecture & system flow  |
| **Sreeja Ganguly** *(Member)*          | St. Xavier’s University            | 🔎 API Research – JWT, OpenRouter, Auth mechanisms  |
| **Sampritee Mandal** *(Member)*        | St. Xavier’s University            | 🗄️ Database Planner – MongoDB schema & collections |

> ✨ A cross-university collaboration under expert guidance!

---

## 📌 Submitted To

**🧑‍🏫 Suruchi Gagan**
*Department of Computer Science, Internship Mentor*

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🛠️ Future Scope

* WebSocket-based live agent routing
* Sentiment-aware responses
* AI fine-tuning for domain-specific replies
* Dashboard for admin statistics and usage metrics

---

## 🙌 Special Thanks

Thanks to the tools and platforms that made this project possible:

* OpenRouter (Claude, GPT)
* MongoDB Atlas
* ReactJS & Flask
* Google Cloud OAuth
* Visual Studio Code

---

