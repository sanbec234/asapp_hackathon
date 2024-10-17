import { useState } from 'react';
import './App.css';
import axios from "axios";

function App() {
  const [question, setQuestion] = useState('');  // State for holding the question
  const [messages, setMessages] = useState([]);  // Store chat messages

  const handleSubmit = async () => {
    if (question.trim() === "") return;
    setMessages([...messages, { type: 'question', text: question }]); // Add question to messages

    try {
      const response = await axios.post('http://localhost:8080/api/question', { question });
      const answer = response.data.answer;
      setMessages(prevMessages => [...prevMessages, { type: 'answer', text: answer }]); // Add answer to messages
    } catch (error) {
      console.error('Error submitting question:', error);
    }

    setQuestion('');  // Clear input after submission
  };

  return (
    <>
      {/* Header section */}
      <header className="app-header">
        <h1>PDFQuery</h1>
      </header>

      <main>
        <h2>Ask your Questions</h2>
        
        <div className="chat-box">
          {/* Display the messages */}
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <p>{message.text}</p>
            </div>
          ))}
        </div>
        
        <div className='user-space'>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your question"
          />
          <button onClick={handleSubmit}>Submit Question</button>
        </div>
      </main>
    </>
  );
}

export default App;
