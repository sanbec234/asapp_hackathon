import { useState, useMemo, useCallback } from 'react';
import './App.css';
import axios from "axios";

function App() {
  const [question, setQuestion] = useState('');  // State for holding the question
  const [messages, setMessages] = useState([]);  // Store chat messages

  // Memoize the messages array to prevent unnecessary recalculations
  const memoizedMessages = useMemo(() => messages, [messages]);

  // Memoize the handleSubmit function using useCallback
  const handleSubmit = useCallback(async () => {
    if (question.trim() === "") return;
    setMessages([...memoizedMessages, { type: 'question', text: question }]); // Add question to messages

    try {
      const response = await axios.post('http://localhost:8080/api/question', { question });
      const answer = response.data.answer;
      setMessages(prevMessages => [...prevMessages, { type: 'answer', text: answer }]); // Add answer to messages
    } catch (error) {
      console.error('Error submitting question:', error);
    }

    setQuestion('');  // Clear input after submission
  }, [question, memoizedMessages]);  // Recreate handleSubmit only if question or memoizedMessages changes

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
          {memoizedMessages.map((message, index) => (
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