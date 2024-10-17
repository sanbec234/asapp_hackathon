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

    // Add user question to messages
    setMessages(prevMessages => [...prevMessages, { type: 'question', text: question }]);
    setLoading(true);

    const controller = new AbortController();
    const signal = controller.signal;

    try {
      // Clean the search query using Gemini API
      const url =
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCcpvCHpUEUagN5OCzkD17wInXFTabpQRQ";
      
      const headers = { "Content-Type": "application/json" };

      const data = {
        contents: [
          {
            parts: [
              {
                text: `return only the redefined version such that the query will be understandable for the Embedding and don't change anything but clean it in terms of typo and grammatical of the following query: "${question}"`,
              },
            ],
          },
        ],
      };

      // Call the Gemini API to clean the query
      const geminiResponse = await axios.post(url, data, { headers });
      const extractedQuery = geminiResponse.data.candidates[0].content.parts[0].text;
      const cleanedQuery = extractedQuery.replace(/json\n|/g, "").trim();

      // Send the cleaned query to your backend
      const response = await axios.post('http://localhost:8080/api/question', { question: cleanedQuery }, { signal });
      const answer = response.data.answer;

      // Add answer to messages
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

    setQuestion(''); // Clear the input after submission
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
