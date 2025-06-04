import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  async query(question, model = null) {
    const response = await apiClient.post('/llm/query', { question, model });
    return response.data;
  },
  
  async initialize(model_name, embedding_model_name, documents_path) {
    const response = await apiClient.post('/llm/initialize', {
      model_name,
      embedding_model_name,
      documents_path
    });
    return response.data;
  },
  
  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/llm/upload-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};
