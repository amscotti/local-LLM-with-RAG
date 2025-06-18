<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>Библиотека документов</h6>
            <input
              type="text"
              class="form-control"
              v-model="searchQuery"
              @input="searchDocuments"
              placeholder="Поиск по названию, описанию или имени файла"
            />
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <div class="folder-structure p-4">
              <!-- Загрузка данных -->
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mt-2">Загрузка данных...</p>
              </div>

              <!-- Сообщение об ошибке -->
              <div v-else-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <!-- Древовидная структура папок на основе тегов -->
              <div v-else>
                <!-- Папка "Без категории" для документов без тега -->
                <div class="folder-item">
                  <div class="folder-header" @click="toggleFolder('untagged')">
                    <i class="fas" :class="openFolders.includes('untagged') ? 'fa-folder-open' : 'fa-folder'"></i>
                    <span class="ms-2">Без категории</span>
                    <span class="badge bg-secondary rounded-pill ms-2">{{ contentData.untagged_content.length }}</span>
                  </div>

                  <!-- Документы без тега -->
                  <div v-if="openFolders.includes('untagged')" class="folder-content ms-4 mt-2">
                    <div v-for="doc in contentData.untagged_content" :key="doc.id" 
                         :class="['document-item py-2', { 'highlight': documents && documents.some(d => d.id === doc.id) }]">
                      <i :class="getFileIconClass(doc.file_path)"></i>
                      <span class="ms-2 fixed-text-container">
                        {{ doc.title || 'Без названия' }} -
                        {{ doc.description || 'Нет описания' }} -
                        {{ getFileName(doc.file_path) }}
                      </span>
                      <button class="btn btn-sm btn-outline-success ms-2" @click="viewDocument(doc)">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button class="btn btn-sm btn-outline-secondary ms-1" @click="downloadDocument(doc)">
                        <i class="fas fa-download"></i>
                      </button>
                      <div class="dropdown ms-1">
                        <button class="btn btn-sm btn-outline-info ms-1" @click="copyLink(doc.id, 'view')">
                          <i class="fas fa-share-alt"></i> Просмотр
                        </button>
                        <button class="btn btn-sm btn-outline-info ms-1" @click="copyLink(doc.id, 'download')">
                          <i class="fas fa-share-alt"></i> Скачать
                        </button>
                      </div>
                    </div>
                    <div v-if="contentData.untagged_content.length === 0" class="text-muted">
                      Нет документов в этой папке
                    </div>
                  </div>
                </div>

                <!-- Папки на основе тегов -->
                <div v-for="tag in contentData.tags" :key="tag.id" class="folder-item">
                  <div class="folder-header" @click="toggleFolder(tag.id)">
                    <i class="fas" :class="openFolders.includes(tag.id) ? 'fa-folder-open' : 'fa-folder'"></i>
                    <span class="ms-2">{{ tag.tag_name }}</span>
                    <span class="badge bg-secondary rounded-pill ms-2">{{ tag.content.length }}</span>
                  </div>

                  <!-- Документы с этим тегом -->
                  <div v-if="openFolders.includes(tag.id)" class="folder-content ms-4 mt-2">
                    <div v-for="doc in tag.content" :key="doc.id" 
                         :class="['document-item py-2', { 'highlight': documents && documents.some(d => d.id === doc.id) }]">
                      <i :class="getFileIconClass(doc.file_path)"></i>
                      <span class="ms-2 fixed-text-container">
                        {{ doc.title || 'Без названия' }} -
                        {{ doc.description || 'Нет описания' }} -
                        {{ getFileName(doc.file_path) }}
                      </span>
                      <button class="btn btn-sm btn-outline-secondary ms-3" @click="viewDocument(doc)">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button class="btn btn-sm btn-outline-secondary ms-3" @click="downloadDocument(doc)">
                        <i class="fas fa-download"></i>
                      </button>
                      <div class="dropdown ms-1">
                        <button class="btn btn-sm btn-outline-info ms-1" @click="copyLink(doc.id, 'view')">
                          <i class="fas fa-share-alt"></i> Просмотр
                        </button>
                        <button class="btn btn-sm btn-outline-info ms-1" @click="copyLink(doc.id, 'download')">
                          <i class="fas fa-share-alt"></i> Скачать
                        </button>
                      </div>
                    </div>
                    <div v-if="tag.content.length === 0" class="text-muted">
                      Нет документов в этой папке
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Модальное окно для просмотра медиа файлов -->
    <div class="modal fade" id="mediaPlayerModal" tabindex="-1" aria-labelledby="mediaPlayerModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="mediaPlayerModalLabel">{{ currentMediaTitle }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center">
            <!-- Аудио плеер -->
            <audio v-if="isAudioFile" controls class="w-100 mb-3" ref="audioPlayer">
              <source :src="currentMediaUrl" :type="currentMediaType">
              Ваш браузер не поддерживает аудио элемент.
            </audio>
            
            <!-- Видео плеер -->
            <video v-if="isVideoFile" controls class="w-100" ref="videoPlayer">
              <source :src="currentMediaUrl" :type="currentMediaType">
              Ваш браузер не поддерживает видео элемент.
            </video>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
            <a :href="currentMediaUrl" download class="btn btn-primary">Скачать</a>
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
  name: "DashboardDefault",
  data() {
    return {
      userId: localStorage.getItem("userId"),
      openFolders: [], // Массив ID открытых папок
      contentData: {
        tags: [],
        untagged_content: []
      },
      loading: true,
      error: null,
      searchQuery: "", // Поле для хранения поискового запроса
      documents: [], // Поле для хранения найденных документов
      mediaPlayerModal: null,
      currentMediaUrl: "",
      currentMediaType: "",
      currentMediaTitle: "",
      isAudioFile: false,
      isVideoFile: false
    };
  },
  async created() {
    if (!this.userId) {
      this.$router.push("/sign-in");
      return;
    }
    
    await this.fetchContentByTags();
  },
  mounted() {
    // Инициализируем модальное окно
    this.mediaPlayerModal = new Modal(document.getElementById('mediaPlayerModal'));
    
    // Добавляем обработчик события закрытия модального окна
    document.getElementById('mediaPlayerModal').addEventListener('hidden.bs.modal', () => {
      // Останавливаем воспроизведение при закрытии модального окна
      if (this.$refs.audioPlayer) {
        this.$refs.audioPlayer.pause();
      }
      if (this.$refs.videoPlayer) {
        this.$refs.videoPlayer.pause();
      }
    });
  },
  methods: {
    async fetchContentByTags() {
      try {
        this.loading = true;
        const response = await axios.get(`http://192.168.81.149:8000/user/${this.userId}/content/by-tags`);
        this.contentData = response.data;

        // Отладка: выводим полученные данные о контенте
        console.log('Полученные данные о контенте:', this.contentData);

        // Выводим информацию о каждом документе
        this.contentData.untagged_content.forEach(doc => {
          console.log(`Документ: ${doc.title}, Описание: ${doc.description}, Путь к файлу: ${doc.file_path}, Имя файла: ${this.getFileName(doc.file_path)}`);
        });

        this.loading = false;
      } catch (error) {
        console.error("Ошибка при получении контента:", error);
        this.error = "Произошла ошибка при загрузке данных";
        this.loading = false;
      }
    },
    async searchDocuments() {
      if (this.searchQuery.length > 0) {
        try {
          const response = await axios.get(`http://192.168.81.149:8000/search-documents?user_id=${this.userId}&search_query=${this.searchQuery}`);
          this.documents = response.data.documents; // Обновляем список документов
        } catch (error) {
          console.error("Ошибка при поиске документов:", error);
          this.error = "Ошибка при поиске документов";
        }
      } else {
        this.documents = []; // Если поле поиска пустое, очищаем список документов
      }
    },
    // Метод для получения имени файла из пути
    getFileName(filePath) {
      if (!filePath) return 'Имя файла недоступно';
      
      // Разделяем путь по слешам и берем последний элемент
      const parts = filePath.split(/[\/\\]/); // Разделяем по / или \
      return parts[parts.length - 1];
    },
    toggleFolder(folderId) {
      if (this.openFolders.includes(folderId)) {
        this.openFolders = this.openFolders.filter(id => id !== folderId);
      } else {
        this.openFolders.push(folderId);
      }
    },
    viewDocument(doc) {
      const fileExtension = this.getFileExtension(doc.file_path);
      
      // Проверяем, является ли файл аудио или видео
      if (this.isAudio(fileExtension) || this.isVideo(fileExtension)) {
        // Настраиваем модальное окно для медиа файла
        this.currentMediaUrl = `http://192.168.81.149:8000/view-file/${doc.id}`;
        this.currentMediaTitle = doc.title || this.getFileName(doc.file_path);
        
        // Устанавливаем тип медиа
        if (this.isAudio(fileExtension)) {
          this.currentMediaType = `audio/${fileExtension}`;
          this.isAudioFile = true;
          this.isVideoFile = false;
        } else if (this.isVideo(fileExtension)) {
          this.currentMediaType = `video/${fileExtension}`;
          this.isAudioFile = false;
          this.isVideoFile = true;
        }
        
        // Открываем модальное окно
        this.mediaPlayerModal.show();
      } else {
        // Для других типов файлов открываем в новой вкладке
        window.open(`http://192.168.81.149:8000/view-file/${doc.id}`, '_blank');
      }
    },
    async downloadDocument(doc) {
      try {
        // Скачивание документа
        window.location.href = `http://192.168.81.149:8000/download-file/${doc.id}`;
      } catch (error) {
        console.error("Ошибка при скачивании документа:", error);
      }
    },
    copyLink(docId, action) {
      const url = action === 'view' 
        ? `http://192.168.81.149:8000/view-file/${docId}` 
        : `http://192.168.81.149:8000/download-file/${docId}`;
      
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
          alert('Ссылка скопирована в буфер обмена!');
        }).catch(err => {
          console.error('Ошибка при копировании ссылки:', err);
        });
      } else {
        // Альтернативный метод копирования для старых браузеров
        const textarea = document.createElement('textarea');
        textarea.value = url;
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand('copy');
          alert('Ссылка скопирована в буфер обмена!');
        } catch (err) {
          console.error('Ошибка при копировании ссылки:', err);
        }
        document.body.removeChild(textarea);
      }
    },
    getFileIconClass(filePath) {
      const extension = this.getFileExtension(filePath);
      switch (extension) {
        case 'pdf':
          return 'fas fa-file-pdf '; // Красный для PDF
        case 'doc':
        case 'docx':
          return 'fas fa-file-word '; // Синий для Word
        case 'xls':
        case 'xlsx':
          return 'fas fa-file-excel'; // Зеленый для Excel
        case 'ppt':
        case 'pptx':
          return 'fas fa-file-powerpoint text-warning'; // Желтый для PowerPoint
        case 'mp3':
        case 'wav':
        case 'ogg':
          return 'fas fa-file-audio text-info'; // Голубой для аудио
        case 'mp4':
        case 'webm':
        case 'avi':
        case 'mov':
          return 'fas fa-file-video text-danger'; // Красный для видео
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'gif':
          return 'fas fa-file-image text-success'; // Зеленый для изображений
        default:
          return 'fas fa-file-alt text-secondary'; // Серый для других форматов
      }
    },
    getFileExtension(filePath) {
      if (!filePath) return '';
      return filePath.split('.').pop().toLowerCase();
    },
    isAudio(extension) {
      return ['mp3', 'wav', 'ogg'].includes(extension);
    },
    isVideo(extension) {
      return ['mp4', 'webm', 'avi', 'mov'].includes(extension);
    }
  }
};
</script>

<style scoped>
.folder-structure {
  font-family: 'Arial', sans-serif;
}

.folder-item {
  margin-bottom: 10px;
}

.folder-header {
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #344767;
  transition: background-color 0.3s;
}

.folder-header:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.document-item {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.document-item:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.fa-folder, .fa-folder-open {
  color: #ffc107;
}

.fa-file-pdf {
  color: rgb(204,20,20);
}

.fa-file-word {
  color: rgb(28,102,228);
}

.fa-file-powerpoint {
  color: rgb(217,101,72);
}

.fa-file-excel {
  color: rgb(35,148,94);
}

.fa-file-audio {
  color: rgb(23,162,184);
}

.fa-file-video {
  color: rgb(220,53,69);
}

.fa-file-image {
  color: rgb(40,167,69);
}

.badge {
  font-size: 0.65em;
}

.fixed-text-container {
  width: 60rem; /* Установите фиксированную ширину */
  overflow: hidden; /* Скрыть переполнение */
  text-overflow: ellipsis; /* Добавить многоточие для длинного текста */
  white-space: nowrap; /* Запретить перенос строк */
}

.highlight {
  background-color: #d1e7dd; /* Цвет фона для подсветки */
}
</style>
