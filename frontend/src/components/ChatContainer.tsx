import React, { useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { LoadingIndicator } from './LoadingIndicator';
import { ChatMessage as ChatMessageType } from '../types';
import { MessageSquare } from 'lucide-react';

interface Props {
  messages: ChatMessageType[];
  isLoading: boolean;
}

export const ChatContainer: React.FC<Props> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
      {messages.length === 0 ? (
        <div className="h-full flex items-center justify-center">
          <div className="text-center max-w-md">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <MessageSquare className="w-8 h-8 text-primary-500" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              Welcome to SAP Process Discovery
            </h2>
            <p className="text-gray-600 mb-6">
              Start a conversation to discover SAP business process mappings.
              Ask me anything!
            </p>
            <div className="space-y-2 text-left">
              <div className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                <p className="text-sm text-gray-700">
                  💡 "Run SAP discovery for vehicle reservation"
                </p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                <p className="text-sm text-gray-700">
                  📊 "Show me the results of the last discovery"
                </p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                <p className="text-sm text-gray-700">
                  📥 "Export the mappings to Excel"
                </p>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && <LoadingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
};
