import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatApp.css';

const ChatApp = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/login', { username, password });
      if (response.data.token) {
        setToken(response.data.token);
        setIsLoggedIn(true);
      }
    } catch (err) {
      // Optionally handle login error
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = { text: input, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        message: input
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const botMessage = { text: response.data.response, sender: 'bot' };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      // Optionally handle chat error
    }
  };

  return (
    <div className="chat-wrapper">
      {!isLoggedIn ? (
        <div className="login-box">
          <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
          <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
          <button onClick={handleLogin}>Login</button>
        </div>
      ) : (
        <div className="chat-box">
          <div className="messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="input-bar">
            <input
              type="text"
              placeholder="Type your message..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatApp; 