<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <authors-table ref="authorsTable" />
      </div>
    </div>
    
    <!-- Таблица контента -->
    <div class="row mt-4">
      <div class="col-12">
        <content-table ref="contentTable" />
      </div>
    </div>
    
    <!-- Админ-панель -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>Панель администратора</h6>
          </div>
          <div class="card-body">
            <ul class="nav nav-tabs" id="adminTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" id="register-tab" data-bs-toggle="tab" data-bs-target="#register" type="button" role="tab" aria-controls="register" aria-selected="true">Регистрация пользователей</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="upload-tab" data-bs-toggle="tab" data-bs-target="#upload" type="button" role="tab" aria-controls="upload" aria-selected="false">Загрузка контента</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="initialize-tab" data-bs-toggle="tab" data-bs-target="#initialize" type="button" role="tab" aria-controls="initialize" aria-selected="false">Инициализация LLM</button>
              </li>
            </ul>
            
            <div class="tab-content mt-3" id="adminTabsContent">
              <!-- Вкладка регистрации пользователей -->
              <div class="tab-pane fade show active" id="register" role="tabpanel" aria-labelledby="register-tab">
                <form @submit.prevent="registerUser">
                  <div class="row">
                    <div class="col-md-4 mb-3">
                      <label for="login" class="form-label">Логин</label>
                      <input type="text" class="form-control" id="login" v-model="registerForm.login" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label for="password" class="form-label">Пароль</label>
                      <input type="password" class="form-control" id="password" v-model="registerForm.password" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label for="role" class="form-label">Роль</label>
                      <select class="form-select" id="role" v-model="registerForm.role_id" required>
                        <option value="1">Администратор</option>
                        <option value="2">Пользователь</option>
                      </select>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="department" class="form-label">Отдел</label>
                      <select class="form-select" id="department" v-model="registerForm.department_id" required>
                        <option v-for="department in departments" :key="department.id" :value="department.id">
                          {{ department.department_name }}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="access" class="form-label">Уровень доступа</label>
                      <select class="form-select" id="access" v-model="registerForm.access_id" required>
                        <option v-for="access in accessLevels" :key="access.id" :value="access.id">
                          {{ access.access_name }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <button type="submit" class="btn bg-gradient-success">Зарегистрировать</button>
                  <div v-if="registerMessage" :class="['alert', registerStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
                    {{ registerMessage }}
                  </div>
                </form>
              </div>
              
              <!-- Вкладка загрузки контента -->
              <div class="tab-pane fade" id="upload" role="tabpanel" aria-labelledby="upload-tab">
                <form @submit.prevent="uploadContent">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="title" class="form-label">Название</label>
                      <input type="text" class="form-control" id="title" v-model="contentForm.title" required>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="file" class="form-label">Файл</label>
                      <input type="file" class="form-control" id="file" @change="handleFileUpload" required>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-12 mb-3">
                      <label for="description" class="form-label">Описание</label>
                      <textarea class="form-control" id="description" rows="3" v-model="contentForm.description"></textarea>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="content-department" class="form-label">Отдел</label>
                      <select class="form-select" id="content-department" v-model="contentForm.department_id" required>
                        <option v-for="department in departments" :key="department.id" :value="department.id">
                          {{ department.department_name }}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="content-access" class="form-label">Уровень доступа</label>
                      <select class="form-select" id="content-access" v-model="contentForm.access_level" required>
                        <option v-for="access in accessLevels" :key="access.id" :value="access.id">
                          {{ access.access_name }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <button type="submit" class="btn bg-gradient-success">Загрузить</button>
                  <div v-if="uploadMessage" :class="['alert', uploadStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
                    {{ uploadMessage }}
                  </div>
                </form>
              </div>
              
              <!-- Вкладка инициализации LLM -->
              <div class="tab-pane fade" id="initialize" role="tabpanel" aria-labelledby="initialize-tab">
                <form @submit.prevent="initializeLLM">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="model-name" class="form-label">Модель LLM</label>
                      <input type="text" class="form-control" id="model-name" v-model="initializeForm.model_name" required placeholder="Введите модель LLM">
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="embedding-model" class="form-label">Модель эмбеддингов</label>
                      <input type="text" class="form-control" id="embedding-model" v-model="initializeForm.embedding_model_name" required placeholder="Введите модель эмбеддингов"></div>
    </div>
    <div class="row">
                    <div class="col-12 mb-3">
                      <label for="documents-path" class="form-label">Путь к документам</label>
                      <input type="text" class="form-control" id="documents-path" v-model="initializeForm.documents_path" placeholder="Например: Research" required>
                      <small class="text-muted">Укажите путь к директории с документами для индексации</small>
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
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthorsTable from "./components/AuthorsTable.vue";
import ContentTable from "./components/ContentTable.vue";
import axios from 'axios';

export default {
  name: "TablesPage",
  components: {
    AuthorsTable,
    ContentTable,
  },
  data() {
    return {
      // Форма регистрации пользователя
      registerForm: {
        login: '',
        password: '',
        role_id: 2,
        department_id: null,
        access_id: null
      },
      registerMessage: '',
      registerStatus: false,
      
      // Форма загрузки контента
      contentForm: {
        title: '',
        description: '',
        department_id: null,
        access_level: null,
        file: null
      },
      uploadMessage: '',
      uploadStatus: false,
      
      // Форма инициализации LLM
      initializeForm: {
        model_name: '',
        embedding_model_name: '',
        documents_path: 'Research',
        confirm: false
      },
      initializeMessage: '',
      initializeStatus: false,
      isInitializing: false,
      
      // Списки для выпадающих меню
      departments: [],
      accessLevels: [],
      llmModels: [],
      embeddingModels: []
    };
  },
  async created() {
    await this.fetchDepartments();
    await this.fetchAccessLevels();
    await this.fetchLLMModels();
    await this.fetchEmbeddingModels();
  },
  methods: {
    // Получение списка отделов
    async fetchDepartments() {
      try {
        const response = await axios.get(`http://192.168.81.149:8000/api/departments`);
        this.departments = response.data;
      } catch (error) {
        console.error('Ошибка при получении отделов:', error);
        this.departments = [];
      }
    },
    
    // Получение списка уровней доступа
    async fetchAccessLevels() {
      try {
        const response = await axios.get(`http://192.168.81.149:8000/api/access_levels`);
        this.accessLevels = response.data;
      } catch (error) {
        console.error('Ошибка при получении отделов:', error);
        this.accessLevels = [];
      }
    },
    
    // Получение списка моделей LLM
    async fetchLLMModels() {
      try {
        const response = await axios.get('http://192.168.81.149:8000/models/llm');
        if (response.data && response.data.models) {
          this.llmModels = response.data.models;
        } else {
          // Fallback на дефолтные значения, если API не вернул моделей
          this.llmModels = [
            'mistral',
            'llama3',
            'ilyagusev/saiga_llama3:latest',
            'gemma'
          ];
        }
      } catch (error) {
        console.error('Ошибка при получении моделей LLM:', error);
        // Fallback на дефолтные значения в случае ошибки
        this.llmModels = [
          'snowflake-arctic-embed2:latest ',
          'llama3',
          'ilyagusev/saiga_llama3',
          'gemma'
        ];
      }
    },
    
    // Получение списка моделей эмбеддингов
    async fetchEmbeddingModels() {
      try {
        const response = await axios.get('http://192.168.81.149:8000/models/embedding');
        if (response.data && response.data.models) {
          this.embeddingModels = response.data.models;
        } else {
          // Fallback на дефолтные значения, если API не вернул моделей
          this.embeddingModels = [
            'snowflake-arctic-embed2:latest ',
            'mxbai-embed-large',
            'all-minilm'
          ];
        }
      } catch (error) {
        console.error('Ошибка при получении моделей эмбеддингов:', error);
        // Fallback на дефолтные значения в случае ошибки
        this.embeddingModels = [
          'snowflake-arctic-embed2:latest',
          'mxbai-embed-large',
          'all-minilm'
        ];
      }
    },
    
    // Регистрация пользователя
    async registerUser() {
      try {
        const response = await axios.post('http://192.168.81.149:8000/register', this.registerForm);
        this.registerMessage = 'Пользователь успешно зарегистрирован!';
        this.registerStatus = true;
        
        // Очистка формы
        this.registerForm = {
          login: '',
          password: '',
          role_id: 2,
          department_id: null,
          access_id: null
        };
        
        // Обновляем список пользователей
        const authorsTableRef = this.$refs.authorsTable;
        if (authorsTableRef && typeof authorsTableRef.fetchUsers === 'function') {
          authorsTableRef.fetchUsers();
        }
      } catch (error) {
        this.registerMessage = error.response?.data?.detail || 'Ошибка при регистрации пользователя';
        this.registerStatus = false;
        console.error('Ошибка регистрации:', error);
      }
    },
    
    // Обработка загрузки файла
    handleFileUpload(event) {
      this.contentForm.file = event.target.files[0];
    },
    
    // Загрузка контента
    async uploadContent() {
      try {
        if (!this.contentForm.title || !this.contentForm.description || !this.contentForm.department_id || 
            !this.contentForm.access_level || !this.contentForm.file) {
          this.uploadMessage = 'Все поля должны быть заполнены';
          this.uploadStatus = false;
          return;
        }

        // Создаем объект FormData для отправки файла
        const formData = new FormData();
        formData.append('file', this.contentForm.file);
        
        // Отправляем запрос с параметрами в URL-строке
        const response = await axios.post(
          `http://192.168.81.149:8000/upload-content?title=${encodeURIComponent(this.contentForm.title)}` +
          `&description=${encodeURIComponent(this.contentForm.description)}` +
          `&access_id=${this.contentForm.access_level}` +
          `&department_id=${this.contentForm.department_id}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        
        this.uploadMessage = 'Контент успешно загружен!';
        this.uploadStatus = true;
        
        // Очистка формы
        this.contentForm = {
          title: '',
          description: '',
          department_id: null,
          access_level: null,
          file: null
        };
        
        // Сбрасываем поле загрузки файла
        document.getElementById('file').value = '';
        
        // Обновляем таблицу контента
        const contentTableRef = this.$refs.contentTable;
        if (contentTableRef && typeof contentTableRef.fetchAllContent === 'function') {
          contentTableRef.fetchAllContent();
        }
        
      } catch (error) {
        this.uploadMessage = error.response?.data?.detail || 'Ошибка при загрузке контента';
        this.uploadStatus = false;
        console.error('Ошибка загрузки контента:', error);
      }
    },
    
    // Инициализация LLM
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
        // Удаляем лишние пробелы из значений
        const modelName = this.initializeForm.model_name.trim();
        const embeddingModelName = this.initializeForm.embedding_model_name.trim();
        const documentsPath = this.initializeForm.documents_path.trim();
        
        // Отладочная информация: выводим параметры, которые отправляем
        console.log('Отправляемые параметры:', {
          model_name: modelName,
          embedding_model_name: embeddingModelName,
          documents_path: documentsPath
        });
        
        const response = await axios.post('http://192.168.81.149:8000/initialize', {
          model_name: modelName,
          embedding_model_name: embeddingModelName,
          documents_path: documentsPath
        });
        
        this.initializeMessage = 'LLM успешно инициализирован!';
        this.initializeStatus = true;
        
        // Сбрасываем подтверждение
        this.initializeForm.confirm = false;
      } catch (error) {
        this.initializeMessage = error.response?.data?.detail || 'Ошибка при инициализации LLM';
        this.initializeStatus = false;
        console.error('Ошибка инициализации LLM:', error);
      } finally {
        this.isInitializing = false;
      }
    }
  }
};
</script>

<style scoped>
.nav-tabs .nav-link {
  color: #344767;
}

.nav-tabs .nav-link.active {
  color: #344767;
  font-weight: 600;
  border-bottom: 2px solid #17c1e8;
}

.form-label {
  color: #344767;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-control, .form-select {
  border: 1px solid #d2d6da;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 400;
  line-height: 1.4rem;
  color: #495057;
  border-radius: 0.5rem;
  transition: 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #82d616;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(130, 214, 22, 0.25);
}
</style>
