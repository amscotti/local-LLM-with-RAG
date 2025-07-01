<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0 text-center">
            <h6>НУЖНО ПРИУМАТЬ НАПОЛНЕНИЕ!!!!</h6>
            
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <div class="p-4 text-center">
              <h1>НУЖНО ПРИУМАТЬ НАПОЛНЕНИЕ!!!!</h1>
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

    <!-- Добавляем кнопку для перехода на страницу библиотеки документов -->
    <div class="row mt-4">
      <div class="col-12 text-center">
        <router-link to="/library" class="btn btn-info me-3">
          <i class="fas fa-book me-2"></i>
          Перейти в библиотеку документов
        </router-link>
        <router-link to="/quizzes" class="btn btn-info">
          <i class="fas fa-clipboard-check me-2"></i>
          Перейти к тестам и анкетам
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  name: "DashboardDefault",
  components: {
    // Удаляем импорт QuizTable
  },
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
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/${this.userId}/content/by-tags`);
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
          const response = await axios.get(`${import.meta.env.VITE_API_URL}/content/search-documents?user_id=${this.userId}&search_query=${this.searchQuery}`);
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
        this.currentMediaUrl = `${import.meta.env.VITE_API_URL}/content/view-file/${doc.id}`;
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
        window.open(`${import.meta.env.VITE_API_URL}/content/view-file/${doc.id}`, '_blank');
      }
    },
    async downloadDocument(doc) {
      try {
        // Скачивание документа
        window.location.href = `${import.meta.env.VITE_API_URL}/content/download-file/${doc.id}`;
      } catch (error) {
        console.error("Ошибка при скачивании документа:", error);
      }
    },
    copyLink(docId, action) {
      const url = action === 'view' 
        ? `${import.meta.env.VITE_API_URL}/content/view-file/${docId}` 
        : `${import.meta.env.VITE_API_URL}/content/download-file/${docId}`;
      
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
.btn-info {
  background-color: #173376;
  border-color: #7b7b7b;
}

</style>
