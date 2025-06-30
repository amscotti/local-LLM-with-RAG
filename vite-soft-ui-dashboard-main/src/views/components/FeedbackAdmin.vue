<template>
  <div class="card">
    <div class="card-header pb-0">
      <div class="row">
        <div class="col-lg-6 col-7">
          <h6>Сообщения обратной связи</h6>
          <p class="text-sm mb-0">
            <i class="fa fa-check text-info" aria-hidden="true"></i>
            <span class="font-weight-bold ms-1">Все сообщения от пользователей</span>
          </p>
        </div>
        <div class="col-lg-6 col-5 my-auto text-end">
          <button @click="fetchFeedbackList" class="btn btn-sm bg-gradient-info mb-0">
            <i class="fas fa-sync-alt me-2"></i>Обновить
          </button>
        </div>
      </div>
    </div>
    <div class="card-body px-0 pt-0 pb-2">
      <!-- Сообщение об ошибке -->
      <div v-if="errorMessage" class="alert alert-danger mx-4 mt-3" role="alert">
        {{ errorMessage }}
      </div>
      
      <!-- Загрузка -->
      <div v-if="isLoading" class="text-center py-5">
        <div class="spinner-border text-info" role="status">
          <span class="visually-hidden">Загрузка...</span>
        </div>
        <p class="mt-2">Загрузка сообщений...</p>
      </div>
      
      <!-- Список сообщений -->
      <div v-else-if="feedbackList.length > 0" class="table-responsive p-0">
        <table class="table align-items-center mb-0">
          <thead>
            <tr>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Пользователь
              </th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                Сообщение
              </th>
              <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Дата
              </th>
              <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Фото
              </th>
              <th class="text-secondary opacity-7"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="feedback in feedbackList" :key="feedback.id">
              <td>
                <div class="d-flex px-2 py-1">
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">{{ feedback.user.full_name || feedback.user.login }}</h6>
                    <p class="text-xs text-secondary mb-0">ID: {{ feedback.user.id }}</p>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-xs font-weight-bold mb-0">
                  {{ truncateText(feedback.text, 100) }}
                </p>
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold">
                  {{ formatDate(feedback.created_at) }}
                </span>
              </td>
              <td class="align-middle text-center">
                <span v-if="feedback.has_photo" class="badge badge-sm bg-gradient-success">Есть</span>
                <span v-else class="badge badge-sm bg-gradient-secondary">Нет</span>
              </td>
              <td class="align-middle">
                <button 
                  @click="viewFeedbackDetails(feedback.id)" 
                  class="btn btn-link text-secondary mb-0"
                >
                  <i class="fas fa-eye text-xs"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Нет сообщений -->
      <div v-else class="text-center py-5">
        <i class="fas fa-inbox fa-3x text-secondary mb-3"></i>
        <p>Сообщений обратной связи пока нет</p>
      </div>
    </div>
    
    <!-- Модальное окно для просмотра деталей -->
    <div class="modal fade" id="feedbackDetailsModal" tabindex="-1" aria-labelledby="feedbackDetailsModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="feedbackDetailsModalLabel">Детали сообщения</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- Загрузка деталей -->
            <div v-if="isLoadingDetails" class="text-center py-4">
              <div class="spinner-border text-info" role="status">
                <span class="visually-hidden">Загрузка...</span>
              </div>
              <p class="mt-2">Загрузка деталей...</p>
            </div>
            
            <!-- Ошибка загрузки деталей -->
            <div v-else-if="detailsError" class="alert alert-danger" role="alert">
              {{ detailsError }}
            </div>
            
            <!-- Детали сообщения -->
            <div v-else-if="currentFeedback" class="p-3">
              <div class="row mb-4">
                <div class="col-md-6">
                  <h6 class="text-sm">Информация о пользователе</h6>
                  <ul class="list-group list-group-flush">
                    <li class="list-group-item d-flex justify-content-between px-0">
                      <span class="text-sm">Имя:</span>
                      <span class="text-sm text-dark font-weight-bold">{{ currentFeedback.user.full_name || 'Не указано' }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between px-0">
                      <span class="text-sm">Логин:</span>
                      <span class="text-sm text-dark font-weight-bold">{{ currentFeedback.user.login }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between px-0">
                      <span class="text-sm">ID пользователя:</span>
                      <span class="text-sm text-dark font-weight-bold">{{ currentFeedback.user.id }}</span>
                    </li>
                  </ul>
                </div>
                <div class="col-md-6">
                  <h6 class="text-sm">Информация о сообщении</h6>
                  <ul class="list-group list-group-flush">
                    <li class="list-group-item d-flex justify-content-between px-0">
                      <span class="text-sm">ID сообщения:</span>
                      <span class="text-sm text-dark font-weight-bold">{{ currentFeedback.id }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between px-0">
                      <span class="text-sm">Дата создания:</span>
                      <span class="text-sm text-dark font-weight-bold">{{ formatDate(currentFeedback.created_at) }}</span>
                    </li>
                    <li class="list-group-item d-flex justify-content-between px-0">
                      <span class="text-sm">Наличие фото:</span>
                      <span class="text-sm text-dark font-weight-bold">
                        <span v-if="currentFeedback.has_photo" class="badge badge-sm bg-gradient-success">Есть</span>
                        <span v-else class="badge badge-sm bg-gradient-secondary">Нет</span>
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
              
              <div class="row mb-4">
                <div class="col-12">
                  <h6 class="text-sm">Текст сообщения</h6>
                  <div class="p-3 border rounded">
                    {{ currentFeedback.text }}
                  </div>
                </div>
              </div>
              
              <div v-if="currentFeedback.has_photo" class="row">
                <div class="col-12">
                  <h6 class="text-sm">Прикрепленное фото</h6>
                  <div class="text-center">
                    <!-- Загрузка фото -->
                    <div v-if="isLoadingPhoto" class="py-3">
                      <div class="spinner-border text-info" role="status">
                        <span class="visually-hidden">Загрузка фото...</span>
                      </div>
                      <p class="mt-2">Загрузка фото...</p>
                    </div>
                    
                    <!-- Ошибка загрузки фото -->
                    <div v-else-if="photoError" class="alert alert-danger" role="alert">
                      {{ photoError }}
                    </div>
                    
                    <!-- Фото -->
                    <img 
                      v-else-if="photoSrc"
                      :src="photoSrc" 
                      alt="Прикрепленное фото" 
                      class="img-fluid rounded" 
                      style="max-height: 400px;"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  name: "FeedbackAdmin",
  data() {
    return {
      feedbackList: [],
      isLoading: true,
      errorMessage: '',
      currentFeedback: null,
      isLoadingDetails: false,
      detailsError: '',
      feedbackModal: null,
      photoSrc: null,
      isLoadingPhoto: false,
      photoError: null
    };
  },
  mounted() {
    this.fetchFeedbackList();
  },
  methods: {
    async fetchFeedbackList() {
      this.isLoading = true;
      this.errorMessage = '';
      
      try {
        const response = await axios.get('/feedback/list');
        this.feedbackList = response.data.feedback_list;
      } catch (error) {
        console.error('Ошибка при загрузке списка сообщений:', error);
        this.errorMessage = error.response?.data?.detail || 'Произошла ошибка при загрузке сообщений';
      } finally {
        this.isLoading = false;
      }
    },
    
    async viewFeedbackDetails(feedbackId) {
      this.isLoadingDetails = true;
      this.detailsError = '';
      this.currentFeedback = null;
      this.photoSrc = null;
      this.photoError = null;
      
      try {
        const response = await axios.get(`/feedback/detail/${feedbackId}`);
        this.currentFeedback = response.data;
        
        // Открываем модальное окно
        if (!this.feedbackModal) {
          this.feedbackModal = new Modal(document.getElementById('feedbackDetailsModal'));
        }
        this.feedbackModal.show();
        
        // Если есть фото, загружаем его
        if (this.currentFeedback.has_photo) {
          this.loadFeedbackPhoto(feedbackId);
        }
      } catch (error) {
        console.error('Ошибка при загрузке деталей сообщения:', error);
        this.detailsError = error.response?.data?.detail || 'Произошла ошибка при загрузке деталей сообщения';
      } finally {
        this.isLoadingDetails = false;
      }
    },
    
    async loadFeedbackPhoto(feedbackId) {
      this.isLoadingPhoto = true;
      this.photoError = null;
      
      try {
        // Загружаем фото как Blob
        const response = await axios.get(`/feedback/photo/${feedbackId}`, {
          responseType: 'blob'
        });
        
        // Создаем URL для Blob
        const blob = new Blob([response.data], { type: response.data.type });
        this.photoSrc = URL.createObjectURL(blob);
      } catch (error) {
        console.error('Ошибка при загрузке фото:', error);
        this.photoError = 'Не удалось загрузить фото';
      } finally {
        this.isLoadingPhoto = false;
      }
    },
    
    truncateText(text, maxLength) {
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + '...';
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('ru-RU');
    }
  }
};
</script> 