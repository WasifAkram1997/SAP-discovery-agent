import React, { useState, useEffect } from 'react';
import { Bot } from 'lucide-react';

export const LoadingIndicator: React.FC = () => {
  const [showHint, setShowHint] = useState(false);

  useEffect(() => {
    // Show hint after 5 seconds for long-running processes
    const timer = setTimeout(() => {
      setShowHint(true);
    }, 5000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="flex gap-3 mb-4">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
        <Bot className="w-5 h-5 text-gray-600" />
      </div>
      <div className="chat-bubble chat-bubble-assistant">
        <div className="flex items-center gap-3">
          <div className="loading-dots text-gray-500">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span className="text-gray-600 text-sm">
            {showHint ? 'Still thinking, this may take a while...' : 'Thinking...'}
          </span>
        </div>
        {showHint && (
          <div className="mt-2 text-xs text-gray-500">
            <p>⏱️ Large Excel files may take a few minutes to process</p>
          </div>
        )}
      </div>
    </div>
  );
};
