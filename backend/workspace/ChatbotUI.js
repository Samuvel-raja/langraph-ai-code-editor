import React, { useState } from 'react';

const ChatbotUI = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      setInput('');
      // Simulate bot response
      setTimeout(() => {
        setMessages(prevMessages => [...prevMessages, { text: 'Bot response to: ' + input, sender: 'bot' }]);
      }, 1000);
    }
  };

  return (
    <div style={{ width: '400px', border: '1px solid #ccc', borderRadius: '5px', padding: '10px' }}>
      <div style={{ height: '300px', overflowY: 'scroll', marginBottom: '10px' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <strong>{msg.sender === 'user' ? 'You' : 'Bot'}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <input
        type='text'
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' ? handleSend() : null}
        style={{ width: '80%' }}
      />
      <button onClick={handleSend} style={{ width: '18%' }}>Send</button>
    </div>
  );
};

export default ChatbotUI;