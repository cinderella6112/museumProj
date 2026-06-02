export interface Province {
  code: string;
  name: string;
  adcode: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  reply: string;
  provinceCode: string;
  provinceName: string;
  suggestions: string[];
}
