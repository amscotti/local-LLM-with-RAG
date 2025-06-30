<template>
  <div class="py-4 container-fluid" @drop.prevent="handleDrop" @dragover.prevent>
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>Обратная связь</h6>
            <p class="text-sm mb-0">
              Отправьте нам сообщение, и мы обязательно его рассмотрим
            </p>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <div class="container">
              <!-- Форма обратной связи -->
              <div class="row mt-4">
                <div class="col-12 col-md-8 mx-auto">
                  <form @submit.prevent="submitFeedback" enctype="multipart/form-data">
                    <!-- Сообщение об успешной отправке -->
                    <div v-if="successMessage" class="alert alert-success" role="alert">
                      {{ successMessage }}
                    </div>
                    
                    <!-- Сообщение об ошибке -->
                    <div v-if="errorMessage" class="alert alert-danger" role="alert">
                      {{ errorMessage }}
                    </div>
                    
                    <!-- Текст сообщения -->
                    <div class="form-group mb-4">
                      <label for="feedbackText" class="form-control-label">Ваше сообщение</label>
                      <textarea 
                        id="feedbackText" 
                        v-model="feedbackForm.text" 
                        class="form-control" 
                        rows="5" 
                        placeholder="Опишите ваш вопрос или предложение..."
                        required
                      ></textarea>
                    </div>
                    
                    <!-- Загрузка фото -->
                    <div class="form-group mb-4">
                      <label for="feedbackPhoto" class="form-control-label">Прикрепить фото (необязательно)</label>
                      <input 
                        type="file" 
                        id="feedbackPhoto" 
                        class="form-control" 
                        @change="handleFileUpload" 
                        accept="image/*"
                      />
                      
                      <!-- Предпросмотр фото -->
                      <div v-if="previewImage" class="mt-3">
                        <img :src="previewImage" alt="Предпросмотр" class="img-fluid" style="max-height: 200px;" />
                        <button type="button" class="btn btn-sm btn-danger mt-2" @click="removeImage">
                          Удалить фото
                        </button>
                      </div>
                    </div>
                    
                    <!-- Кнопка отправки -->
                    <div class="d-flex justify-content-end">
                      <button 
                        type="submit" 
                        class="btn bg-gradient-info" 
                        :disabled="isSubmitting"
                      >
                        <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        {{ isSubmitting ? 'Отправка...' : 'Отправить сообщение' }}
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Feedback",
  data() {
    return {
      feedbackForm: {
        text: '',
      },
      selectedFile: null,
      previewImage: null,
      isSubmitting: false,
      successMessage: '',
      errorMessage: '',
      userId: localStorage.getItem('userId') || null
    };
  },
  mounted() {
    // Проверка авторизации
    if (!this.userId) {
      this.$router.push('/sign-in');
    }
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      // Проверка типа файла
      if (!file.type.match('image.*')) {
        this.errorMessage = 'Пожалуйста, выберите изображение';
        return;
      }
      
      // Ограничение размера файла (5 МБ)
      if (file.size > 10 * 1024 * 1024) {
        this.errorMessage = 'Размер файла не должен превышать 5 МБ';
        return;
      }
      
      this.selectedFile = file;
      this.errorMessage = '';
      
      // Создаем предпросмотр изображения
      const reader = new FileReader();
      reader.onload = (e) => {
        this.previewImage = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    handleDrop(event) {
      const files = event.dataTransfer.files;
      if (files.length) {
        this.handleFileUpload({ target: { files } });
      }
    },
    removeImage() {
      this.selectedFile = null;
      this.previewImage = null;
      // Сбрасываем поле выбора файла
      document.getElementById('feedbackPhoto').value = '';
    },
    async submitFeedback() {
      if (!this.feedbackForm.text.trim()) {
        this.errorMessage = 'Пожалуйста, введите текст сообщения';
        return;
      }
      
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        // Создаем объект FormData для отправки данных
        const formData = new FormData();
        formData.append('user_id', this.userId);
        formData.append('text', this.feedbackForm.text);
        
        // Добавляем файл, если он выбран
        if (this.selectedFile) {
          formData.append('photo', this.selectedFile);
        }
        
        // Отправляем запрос
        const response = await axios.post('/feedback/create', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        // Обрабатываем успешный ответ
        this.successMessage = 'Ваше сообщение успешно отправлено!';
        
        // Сбрасываем форму
        this.feedbackForm.text = '';
        this.removeImage();
        
      } catch (error) {
        console.error('Ошибка при отправке сообщения:', error);
        this.errorMessage = error.response?.data?.detail || 'Произошла ошибка при отправке сообщения';
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.form-control:focus {
  border-color: #5e72e4;
  box-shadow: 0 0 0 0.2rem rgba(94, 114, 228, 0.25);
}
</style> 