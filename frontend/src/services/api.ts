import axios from 'axios'
import type { ChatRequest, ChatResponse } from '@/types'

const apiClient = axios.create({
  // 👇 换成读取环境变量，如果读不到就用默认的 localhost
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000', 
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const sendQuestion = async (data: ChatRequest): Promise<ChatResponse> => {
  const response = await apiClient.post<ChatResponse>('/api/chat', data)
  return response.data
}