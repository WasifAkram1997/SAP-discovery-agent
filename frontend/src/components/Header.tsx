import React from 'react';
import { Search, Activity, Trash2 } from 'lucide-react';

interface Props {
  onClearChat: () => void;
  isHealthy: boolean;
}

export const Header: React.FC<Props> = ({ onClearChat, isHealthy }) => {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
            <Search className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              SAP Process Discovery Agent
            </h1>
            <p className="text-sm text-gray-500">
              Chat with AI to discover SAP business processes
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Health status indicator */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100">
            <Activity
              className={`w-4 h-4 ${
                isHealthy ? 'text-green-500' : 'text-red-500'
              }`}
            />
            <span className="text-sm font-medium text-gray-700">
              {isHealthy ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* Clear chat button */}
          <button
            onClick={onClearChat}
            className="btn-secondary flex items-center gap-2"
            title="Clear chat history"
          >
            <Trash2 className="w-4 h-4" />
            <span>Clear</span>
          </button>
        </div>
      </div>
    </header>
  );
};
