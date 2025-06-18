<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>Библиотека документов</h6>
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
                    <div v-for="doc in contentData.untagged_content" :key="doc.id" class="document-item py-2">
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
                    <div v-for="doc in tag.content" :key="doc.id" class="document-item py-2">
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
  </div>
</template>

<script>
import axios from 'axios';

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
      error: null
    };
  },
  async created() {
    if (!this.userId) {
      this.$router.push("/sign-in");
      return;
    }
    
    await this.fetchContentByTags();
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
      // Открытие документа для просмотра
      window.open(`http://192.168.81.149:8000/view-file/${doc.id}`, '_blank');
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
      const extension = filePath.split('.').pop().toLowerCase();
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
        default:
          return 'fas fa-file-alt text-secondary'; // Серый для других форматов
      }
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

.badge {
  font-size: 0.65em;
}

.fixed-text-container {
  width: 60rem; /* Установите фиксированную ширину */
  overflow: hidden; /* Скрыть переполнение */
  text-overflow: ellipsis; /* Добавить многоточие для длинного текста */
  white-space: nowrap; /* Запретить перенос строк */
}
</style>
