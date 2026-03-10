import axios from 'axios';
import type { Document, DocumentCreate, DocumentUpdate } from '@/types/document';

const apiClient = axios.create({
  baseURL: '/api', // через прокси
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use(request => {
  console.log('➡️ Запрос:', request.method?.toUpperCase(), request.url, request.data);
  return request;
});

// Логирование ответов и ошибок
apiClient.interceptors.response.use(
  response => {
    console.log('✅ Ответ:', response.status, response.data);
    return response;
  },
  error => {
    console.error('❌ Ошибка ответа:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

export default {
  // Получить список документов с фильтром и пагинацией
  getDocuments(skip = 0, limit = 100, status?: string) {
    const params: Record<string, any> = { skip, limit };
    if (status) params.status = status;
    return apiClient.get<Document[]>('/documents/', { params });
  },

  // Получить документ по ID
  getDocument(id: number) {
    return apiClient.get<Document>(`/documents/${id}`);
  },

  // Создать новый документ
  createDocument(data: DocumentCreate) {
    return apiClient.post<Document>('/documents/', data);
  },

  // Обновить документ
  updateDocument(id: number, data: DocumentUpdate) {
    return apiClient.put<Document>(`/documents/${id}`, data);
  },

  // Удалить документ
  deleteDocument(id: number) {
    return apiClient.delete(`/documents/${id}`);
  }
};