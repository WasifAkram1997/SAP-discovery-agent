import React from 'react';
import { ChatMessage as ChatMessageType } from '../types';
import { User, Bot } from 'lucide-react';
import { formatContent } from '../utils/formatContent';

interface Props {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<Props> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 mb-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary-500' : 'bg-gray-200'
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-gray-600" />
        )}
      </div>

      {/* Message bubble */}
      <div
        className={`chat-bubble ${
          isUser ? 'chat-bubble-user' : 'chat-bubble-assistant'
        }`}
      >
        <div className={isUser ? 'text-white' : 'text-gray-800'}>
          {formatContent(message.content)}
        </div>
        <div
          className={`text-xs mt-1 ${
            isUser ? 'text-primary-100' : 'text-gray-400'
          }`}
        >
          {message.timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>
    </div>
  );
};
