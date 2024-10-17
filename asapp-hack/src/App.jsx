import { useState, useMemo, useCallback } from 'react';
import './App.css';
import axios from "axios";

function App() {
  const [question, setQuestion] = useState('');  
  const [messages, setMessages] = useState([]);  
  const [loading, setLoading] = useState(false);  

  const memoizedMessages = useMemo(() => messages, [messages]);

  const handleSubmit = useCallback(async () => {
    if (question.trim() === "") return;

    setMessages(prevMessages => [...prevMessages, { type: 'question', text: question }]);
    setLoading(true);

    const controller = new AbortController();
    const signal = controller.signal;

    try {
      const response = await axios.post('http://localhost:8080/api/question', { question }, { signal });
      const answer = response.data.answer;
      setMessages(prevMessages => [...prevMessages, { type: 'answer', text: answer }]);
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log('Request canceled:', error.message);
      } else {
        console.error('Error submitting question:', error);
        setMessages(prevMessages => [...prevMessages, { type: 'answer', text: 'Error getting response.' }]);
      }
    } finally {
      setLoading(false);
    }

    setQuestion('');
    return () => {
      controller.abort();
    };
  }, [question]);

  return (
    <div className="app">
      <header className="app-header">
        <h1>ASAPP</h1>
      </header>

      <main className="main-content">
        <div className="chat-box">
          {memoizedMessages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <p>{message.text}</p>
            </div>
          ))}
          {loading && 
            <div className="loading-container">
              <div className="spinner"></div>
            </div>
          }
        </div>

        <div className="input-area">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter a prompt for ASAPP"
            className="input-box"
            rows="3"  // Adjust the number of visible rows as needed
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault(); // Prevent the default behavior of Enter key
                handleSubmit(); // Submit the question
              }
            }}
            />
          <button onClick={handleSubmit} className="submit-button">Send</button>
        </div>
      </main>
    </div>
  );
}

export default App;
