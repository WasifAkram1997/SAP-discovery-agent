import React from 'react';
import { Info, Zap, FileText, Download, Play } from 'lucide-react';

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-80 bg-white border-l border-gray-200 p-6 overflow-y-auto custom-scrollbar">
      <div className="space-y-6">
        {/* Info Section */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <Info className="w-5 h-5 text-primary-500" />
            <h2 className="font-semibold text-gray-900">Information</h2>
          </div>
          <p className="text-sm text-gray-600 leading-relaxed">
            This chat interface connects to the SAP Process Discovery Agent API.
            Ask questions about SAP processes and get detailed mappings.
          </p>
        </div>

        {/* Features */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <Zap className="w-5 h-5 text-primary-500" />
            <h2 className="font-semibold text-gray-900">Features</h2>
          </div>
          <ul className="space-y-2 text-sm text-gray-600">
            <li className="flex items-start gap-2">
              <span className="text-primary-500 mt-0.5">•</span>
              <span>Ask questions about SAP processes</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary-500 mt-0.5">•</span>
              <span>Run SAP discovery on business processes</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary-500 mt-0.5">•</span>
              <span>View detailed process mappings</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary-500 mt-0.5">•</span>
              <span>Export results to Excel format</span>
            </li>
          </ul>
        </div>

        {/* Commands */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <FileText className="w-5 h-5 text-primary-500" />
            <h2 className="font-semibold text-gray-900">Sample Commands</h2>
          </div>
          <div className="space-y-2">
            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2 text-primary-600 font-medium text-sm mb-1">
                <Play className="w-3 h-3" />
                <span>Run Discovery</span>
              </div>
              <code className="text-xs text-gray-600">
                "Run SAP discovery"
              </code>
            </div>

            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2 text-primary-600 font-medium text-sm mb-1">
                <FileText className="w-3 h-3" />
                <span>View Results</span>
              </div>
              <code className="text-xs text-gray-600">
                "Display the results"
              </code>
            </div>

            <div className="p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2 text-primary-600 font-medium text-sm mb-1">
                <Download className="w-3 h-3" />
                <span>Export Data</span>
              </div>
              <code className="text-xs text-gray-600">
                "Export to Excel"
              </code>
            </div>
          </div>
        </div>

        {/* Quick Tips */}
        <div className="p-4 bg-primary-50 rounded-lg border border-primary-100">
          <h3 className="font-semibold text-primary-900 text-sm mb-2">
            💡 Quick Tip
          </h3>
          <p className="text-xs text-primary-700 leading-relaxed">
            You can combine commands like "Run and print" to execute discovery
            and display results in one go. The agent uses advanced LangGraph
            workflow for accurate SAP mappings.
          </p>
        </div>

        {/* Technical Info */}
        <div className="pt-4 border-t border-gray-200">
          <div className="text-xs text-gray-500 space-y-1">
            <div className="flex justify-between">
              <span>API Endpoint:</span>
              <span className="font-mono">/api</span>
            </div>
            <div className="flex justify-between">
              <span>Status:</span>
              <span className="text-green-600 font-medium">Active</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};
