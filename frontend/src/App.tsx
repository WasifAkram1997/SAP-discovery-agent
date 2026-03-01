import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ChatContainer } from './components/ChatContainer';
import { ChatInput } from './components/ChatInput';
import { Sidebar } from './components/Sidebar';
import { ChatMessage } from './types';
import { api } from './services/api';
import { AlertCircle } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isHealthy, setIsHealthy] = useState(false);

  // Check API health on mount
  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const health = await api.getHealth();
      setIsHealthy(health.agent && health.status === 'healthy');
    } catch (error) {
      setIsHealthy(false);
      console.error('Health check failed:', error);
    }
  };

  const handleSendMessage = async (message: string, file?: File) => {
    // Display user message with file indicator if present
    const userContent = file
      ? `${message}\n\n📎 Attached: ${file.name}`
      : message;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: userContent,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.sendMessage(message, file);

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);

      const errorResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `❌ Error: ${errorMessage}\n\nPlease make sure the API backend is running on http://localhost:8001`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      setMessages([]);
      setError(null);
    }
  };

  return (
    <div className="h-screen flex flex-col">
      <Header onClearChat={handleClearChat} isHealthy={isHealthy} />

      <div className="flex-1 flex overflow-hidden">
        {/* Main chat area */}
        <div className="flex-1 flex flex-col">
          {/* Error banner */}
          {error && !isHealthy && (
            <div className="bg-red-50 border-b border-red-200 px-6 py-3">
              <div className="flex items-center gap-2 text-red-800">
                <AlertCircle className="w-5 h-5" />
                <span className="text-sm font-medium">
                  Cannot connect to API. Make sure the backend is running on http://localhost:8001
                </span>
              </div>
            </div>
          )}

          <ChatContainer messages={messages} isLoading={isLoading} />
          <ChatInput onSend={handleSendMessage} disabled={isLoading} />
        </div>

        {/* Sidebar */}
        <Sidebar />
      </div>
    </div>
  );
}

export default App;
