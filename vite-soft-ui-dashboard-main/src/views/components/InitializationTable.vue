<template>
  <div>
    <form @submit.prevent="initializeLLM">
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="model-name" class="form-label">Модель LLM</label>
          <input type="text" class="form-control" id="model-name" v-model="initializeForm.model_name" required placeholder="Введите модель LLM">
        </div>
        <div class="col-md-6 mb-3">
          <label for="embedding-model" class="form-label">Модель эмбеддингов</label>
          <input type="text" class="form-control" id="embedding-model" v-model="initializeForm.embedding_model_name" required placeholder="Введите модель эмбеддингов">
        </div>
      </div>
      <div class="row">
        <div class="col-12 mb-3">
          <label for="documents-path" class="form-label">Путь к документам</label>
          <input type="text" class="form-control" id="documents-path" v-model="initializeForm.documents_path" placeholder="Например: Research" required>
          <small class="text-muted">Укажите путь к директории с документами для индексации</small>
        </div>
      </div>
      <div class="row">
        <div class="col-12 mb-3">
          <label for="department-id" class="form-label">Идентификатор отдела</label>
          <input type="text" class="form-control" id="department-id" v-model="initializeForm.department_id" required placeholder="Введите идентификатор отдела">
          <small class="text-muted">Укажите идентификатор отдела для создания уникальной базы данных</small>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-12">
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="confirm-init" v-model="initializeForm.confirm">
            <label class="form-check-label" for="confirm-init">
              Я подтверждаю, что хочу инициализировать LLM. Это может занять некоторое время.
            </label>
          </div>
        </div>
      </div>
      <button type="submit" class="btn bg-gradient-success" :disabled="!initializeForm.confirm || isInitializing">
        <span v-if="isInitializing" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        {{ isInitializing ? 'Инициализация...' : 'Инициализировать LLM' }}
      </button>
      <div v-if="initializeMessage" :class="['alert', initializeStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
        {{ initializeMessage }}
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LLMInitialization',
  data() {
    return {
      initializeForm: {
        model_name: '',
        embedding_model_name: '',
        documents_path: 'Research',
        confirm: false,
        department_id: null
      },
      initializeMessage: '',
      initializeStatus: false,
      isInitializing: false,
    };
  },
  methods: {
    async initializeLLM() {
      if (!this.initializeForm.confirm) {
        this.initializeMessage = 'Пожалуйста, подтвердите инициализацию';
        this.initializeStatus = false;
        return;
      }
      
      this.isInitializing = true;
      this.initializeMessage = 'Идет инициализация LLM, это может занять некоторое время...';
      this.initializeStatus = true;
      
      try {
        const modelName = this.initializeForm.model_name.trim();
        const embeddingModelName = this.initializeForm.embedding_model_name.trim();
        const documentsPath = this.initializeForm.documents_path.trim();
        const departmentId = this.initializeForm.department_id.trim();
        
        if (!departmentId) {
          this.initializeMessage = 'ID отдела не может быть пустым';
          this.initializeStatus = false;
          this.isInitializing = false;
          return;
        }
        
        const requestData = {
          model_name: modelName,
          embedding_model_name: embeddingModelName,
          documents_path: documentsPath,
          department_id: departmentId
        };
        
        const response = await axios.post('http://192.168.81.149:8000/llm/initialize', requestData);
        
        this.initializeMessage = 'LLM успешно инициализирован!';
        this.initializeStatus = true;
        this.initializeForm.confirm = false;
      } catch (error) {
        this.initializeMessage = 'Ошибка инициализации LLM: ' + (error.response?.data?.detail || error.message);
        this.initializeStatus = false;
        console.error('Ошибка инициализации LLM:', error);
      } finally {
        this.isInitializing = false;
      }
    }
  },
  mounted() {
    // Логика инициализации
  }
};
</script>

<style scoped>
/* Ваши стили */
</style>
