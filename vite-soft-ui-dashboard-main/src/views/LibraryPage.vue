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
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mt-2">Загрузка данных...</p>
              </div>
              <div v-else-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              <div v-else>
                <div v-if="documents.length > 0">
                  <h6>Результаты поиска:</h6>
                  <div v-for="doc in documents" :key="doc.id" class="document-item">
                    <div class="document-header">
                      <h6>{{ doc.title }}</h6>
                      <p>{{ doc.description }}</p>
                      <div class="document-actions">
                        <button class="btn btn-sm btn-info" @click="viewDocument(doc)">
                          <i class="fas fa-eye me-1"></i> Просмотреть
                        </button>
                        <button class="btn btn-sm btn-info ms-2" @click="downloadDocument(doc)">
                          <i class="fas fa-download me-1"></i> Скачать
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <p>Документы не найдены.</p>
                </div>
                <div class="folder-item">
                  <div class="folder-header" @click="openTagPage('untagged')">
                    <i class="fas fa-folder"></i>
                    <span class="ms-2">Без категории</span>
                    <span class="badge bg-secondary rounded-pill ms-2">{{ contentData.untagged_content.length }}</span>
                  </div>
                </div>
                <div v-for="tag in contentData.tags" :key="tag.id" class="folder-item">
                  <div class="folder-header" @click="openTagPage(tag.id, tag.tag_name)">
                    <i class="fas fa-folder"></i>
                    <span class="ms-2">{{ tag.tag_name }}</span>
                    <span class="badge bg-secondary rounded-pill ms-2">{{ tag.content.length }}</span>
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
  name: "LibraryPage",
  data() {
    return {
      userId: localStorage.getItem("userId"),
      contentData: {
        tags: [],
        untagged_content: []
      },
      loading: true,
      error: null,
      searchQuery: "",
      documents: []
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
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/${this.userId}/content/by-tags`);
        this.contentData = response.data;
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
          this.documents = response.data.documents;
        } catch (error) {
          console.error("Ошибка при поиске документов:", error);
          this.error = "Ошибка при поиске документов";
        }
      } else {
        this.documents = [];
      }
    },
    openTagPage(tagId, tagName = 'Без категории') {
      this.$router.push({ 
        name: 'TagContent', 
        params: { 
          tagId: tagId,
          tagName: tagName
        } 
      });
    },
    viewDocument(doc) {
      // Открываем документ для просмотра
      window.open(`${import.meta.env.VITE_API_URL}/content/view-file/${doc.id}`, '_blank');
    },
    downloadDocument(doc) {
      // Скачиваем документ
      window.location.href = `${import.meta.env.VITE_API_URL}/content/download-file/${doc.id}`;
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

.fa-folder, .fa-folder-open {
  color: #ffc107;
}

.badge {
  font-size: 0.65em;
}
.document-item {
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-bottom: 10px;
}
.document-header {
  font-weight: bold;
}
.document-actions {
  margin-top: 10px;
}
.btn-info {
  background-color: #173376;
  border-color: #7b7b7b;
}
.form-control:focus {
  border-color: #5e72e4;
  box-shadow: 0 0 0 0.2rem rgba(94, 114, 228, 0.25);
}

</style> 