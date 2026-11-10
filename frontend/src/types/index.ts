// 定义前端发给后端的请求格式
export interface ChatRequest {
  question: string;
}

// 定义后端返回给前端的响应格式
export interface ChatResponse {
  success: boolean;
  answer: string;
}