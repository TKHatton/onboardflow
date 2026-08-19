import { useState } from 'react';
import { onboardAPI } from '../api';
import './Chatbot.css';

interface ChatMessage {
  id: string;
  type: 'user' | 'bot';
  text: string;
  timestamp: Date;
  resources?: Array<{ title: string; url: string }>;
}

interface ChatbotProps {
  employeeName: string;
  employeeContext?: any;
}

export function Chatbot({ employeeName, employeeContext }: ChatbotProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      type: 'bot',
      text: `Hi ${employeeName}! I'm your onboarding assistant. Ask me anything about your onboarding process, benefits, training, or company policies.`,
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      text: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await onboardAPI.chat(employeeName, input, employeeContext);
      
      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        text: response.data.answer,
        timestamp: new Date(),
        resources: response.data.resources,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        text: 'Sorry, I encountered an error. Please try again or contact HR directly.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQuestions = [
    'When will I receive my equipment?',
    'How do I enroll in benefits?',
    'What training do I need to complete?',
    'How do I request time off?',
  ];

  return (
    <div className="chatbot">
      <div className="chatbot-header">
        <h3>💬 Onboarding Assistant</h3>
        <p>Ask me anything about your onboarding</p>
      </div>

      <div className="chatbot-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.type}`}>
            <div className="message-content">
              <p>{msg.text}</p>
              {msg.resources && msg.resources.length > 0 && (
                <div className="message-resources">
                  <strong>Related resources:</strong>
                  <ul>
                    {msg.resources.map((resource, idx) => (
                      <li key={idx}>
                        <a href={resource.url} target="_blank" rel="noopener noreferrer">
                          {resource.title}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            <div className="message-time">
              {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="chatbot-quick-questions">
        {quickQuestions.map((question, idx) => (
          <button
            key={idx}
            className="quick-question-btn"
            onClick={() => {
              setInput(question);
              setTimeout(handleSend, 100);
            }}
            disabled={isLoading}
          >
            {question}
          </button>
        ))}
      </div>

      <div className="chatbot-input">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your question..."
          disabled={isLoading}
          rows={2}
        />
        <button onClick={handleSend} disabled={isLoading || !input.trim()}>
          {isLoading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
