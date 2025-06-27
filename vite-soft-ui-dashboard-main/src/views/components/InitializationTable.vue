<template>
  <div>
    <!-- Навигация по подвкладкам -->
    <ul class="nav nav-pills mb-3" id="llmTabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="init-llm-tab" data-bs-toggle="pill" data-bs-target="#init-llm" type="button" role="tab" aria-controls="init-llm" aria-selected="true">Инициализация LLM</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="create-dir-tab" data-bs-toggle="pill" data-bs-target="#create-dir" type="button" role="tab" aria-controls="create-dir" aria-selected="false">Создание директории</button>
      </li>
    </ul>
    
    <!-- Содержимое подвкладок -->
    <div class="tab-content" id="llmTabsContent">
      <!-- Вкладка инициализации LLM -->
      <div class="tab-pane fade show active" id="init-llm" role="tabpanel" aria-labelledby="init-llm-tab">
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
      
      <!-- Вкладка создания директории -->
      <div class="tab-pane fade" id="create-dir" role="tabpanel" aria-labelledby="create-dir-tab">
        <form @submit.prevent="createDirectory">
          <div class="row">
            <div class="col-12 mb-3">
              <label for="dir-path" class="form-label">Путь к директории</label>
              <input type="text" class="form-control" id="dir-path" v-model="directoryForm.path" required placeholder="Например: Research/SubFolder">
              <small class="text-muted">Укажите путь, где должна быть создана директория</small>
            </div>
          </div>
          <button type="submit" class="btn btn-info" :disabled="isCreatingDirectory">
            <span v-if="isCreatingDirectory" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            {{ isCreatingDirectory ? 'Создание...' : 'Создать директорию' }}
          </button>
          <div v-if="directoryMessage" :class="['alert', directoryStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
            {{ directoryMessage }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as bootstrap from 'bootstrap';

export default {
  name: 'LLMInitialization',
  data() {
    return {
      // Данные для инициализации LLM
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
      
      // Данные для создания директории
      directoryForm: {
        path: ''
      },
      directoryMessage: '',
      directoryStatus: false,
      isCreatingDirectory: false
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
        
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/llm/initialize`, requestData);
        
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
    },
    
    // Метод для создания директории
    async createDirectory() {
      this.isCreatingDirectory = true;
      this.directoryMessage = 'Создание директории...';
      this.directoryStatus = true;
      
      try {
        const dirPath = this.directoryForm.path.trim();
        
        if (!dirPath) {
          this.directoryMessage = 'Путь директории не может быть пустым';
          this.directoryStatus = false;
          this.isCreatingDirectory = false;
          return;
        }
        
        // Отладочный вывод
        console.log('Отправляемые данные на эндпоинт /create, путь директории:', dirPath);
        
        // Используем параметры запроса вместо JSON-тела
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/directory/create?directory_path=${encodeURIComponent(dirPath)}`);
        
        this.directoryMessage = 'Директория успешно создана!';
        this.directoryStatus = true;
        
        // Очистка формы после успешного создания
        this.directoryForm.path = '';
      } catch (error) {
        this.directoryMessage = 'Ошибка создания директории: ' + (error.response?.data?.detail || error.message);
        this.directoryStatus = false;
        console.error('Ошибка создания директории:', error);
      } finally {
        this.isCreatingDirectory = false;
      }
    }
  },
  mounted() {
    // Инициализация Bootstrap компонентов
    const tabElements = document.querySelectorAll('#llmTabs [data-bs-toggle="pill"]');
    tabElements.forEach(tabElement => {
      new bootstrap.Tab(tabElement);
    });
  }
};
</script>

<style scoped>
.nav-pills .nav-link {
  color: #344767;
  border-radius: 0.5rem;
}

.nav-pills .nav-link.active {
  background-color: #17c1e8;
  color: #fff;
  box-shadow: 0 4px 6px rgba(50, 50, 93, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.form-label {
  color: #344767;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.btn-info {
  background-color: #173376;
  border-color: #7b7b7b;
}
</style>
