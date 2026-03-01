export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
}

export interface SAPProcessMapping {
  process: string;
  module: string[];
  transaction_codes: string[];
  fiori_apps: string[];
  execution_flow: string[];
  configuration_dependencies: string[];
  integration_points: string[];
  references: Reference[];
}

export interface Reference {
  title: string;
  url: string;
  source: string;
}

export interface HealthStatus {
  status: string;
  agent: boolean;
  timestamp: string;
}
