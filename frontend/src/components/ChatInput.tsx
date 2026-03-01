import React, { useState, KeyboardEvent, useRef } from 'react';
import { Send, Paperclip, X } from 'lucide-react';

interface Props {
  onSend: (message: string, file?: File) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<Props> = ({ onSend, disabled = false }) => {
  const [input, setInput] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim(), selectedFile || undefined);
      setInput('');
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      const validTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
      ];
      if (validTypes.includes(file.type) || file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
        setSelectedFile(file);
      } else {
        alert('Please select an Excel file (.xlsx or .xls)');
      }
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      {/* File preview */}
      {selectedFile && (
        <div className="mb-3 flex items-center gap-2 bg-blue-50 border border-blue-200 rounded-lg px-3 py-2">
          <Paperclip className="w-4 h-4 text-blue-600" />
          <span className="text-sm text-blue-900 flex-1">{selectedFile.name}</span>
          <button
            onClick={handleRemoveFile}
            className="text-blue-600 hover:text-blue-800 transition-colors"
            title="Remove file"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      <div className="flex gap-2 items-end">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about SAP processes..."
          disabled={disabled}
          rows={1}
          className="input-field resize-none min-h-[48px] max-h-32"
          style={{
            height: 'auto',
            minHeight: '48px',
          }}
          onInput={(e) => {
            const target = e.target as HTMLTextAreaElement;
            target.style.height = 'auto';
            target.style.height = target.scrollHeight + 'px';
          }}
        />

        {/* File upload button */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx,.xls,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"
          onChange={handleFileSelect}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className={`h-12 w-12 flex items-center justify-center flex-shrink-0 rounded-lg border-2 border-gray-300 cursor-pointer transition-colors ${
            disabled ? 'opacity-50 cursor-not-allowed' : 'hover:border-primary-500 hover:bg-primary-50'
          }`}
          title="Upload Excel file"
        >
          <Paperclip className="w-5 h-5 text-gray-600" />
        </label>

        <button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          className="btn-primary h-12 w-12 flex items-center justify-center flex-shrink-0"
          title="Send message"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
      <div className="mt-2 text-xs text-gray-500">
        Press <kbd className="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded text-xs">Enter</kbd> to send, <kbd className="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded text-xs">Shift + Enter</kbd> for new line
      </div>
    </div>
  );
};
