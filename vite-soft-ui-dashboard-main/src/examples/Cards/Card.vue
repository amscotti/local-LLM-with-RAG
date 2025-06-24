<template>
  <div class="m-1 card">
    <div class="p-3 card-body">
      <div class="d-flex align-items-center" :class="directionReverse ? reverseDirection : ''">
        <div class="flex-grow-1">
          <div class="numbers">
            <p class="mb-0 text-sm text-capitalize font-weight-bold" :class="titleColor">{{ content.title }}</p>
            <p class="mb-0 font-weight-bolder" :class="valueColor">{{ content.description }}</p>
            <a :href="getDownloadLink(contentId)" class="text-secondary font-weight-bold text-sm" data-toggle="tooltip" data-original-title="Скачать файл">Скачать</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "CardComponent",
  props: {
    directionReverse: Boolean,
    titleColor: {
      type: String,
      default: ""
    },
    valueColor: {
      type: String,
      default: ""
    },
    percentageColor: {
      type: String,
      default: "text-success",
    },
    contentClass: {
      type: String,
      default: ""
    },
    title: {
      type: String,
      default: ""
    },
    value: {
      type: String,
      default: ""
    },
    percentage: {
      type: String,
      default: ""
    },
    userId: { // Убедитесь, что передаете ID пользователя
      type: Number,
      required: true
    },
    contentId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      content: {
        title: this.title || '',
        description: this.value || '',
        file_path: this.percentage || ''
      },
      reverseDirection: "flex-row-reverse justify-content-between",
    };
  },
  watch: {
    // Следим за изменениями пропсов
    title(newVal) {
      this.content.title = newVal;
    },
    value(newVal) {
      this.content.description = newVal;
    },
    percentage(newVal) {
      this.content.file_path = newVal;
    }
  },
  created() {
    // Инициализируем значения из пропсов
    this.content = {
      title: this.title || '',
      description: this.value || '',
      file_path: this.percentage || ''
    };
    console.log('Initial content:', this.content);
  },
  methods: {
    async fetchContent() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/${this.userId}/content`);
        console.log('Response data:', response.data);
        
        // Проверяем, является ли response.data массивом
        if (Array.isArray(response.data) && response.data.length > 0) {
          // Берем первый элемент массива
          const firstContent = response.data[0];
          this.content = {
            title: firstContent.title || '',
            description: firstContent.description || '',
            file_path: firstContent.file_path || ''
          };
        } else if (typeof response.data === 'object') {
          // Если это объект, используем его напрямую
          this.content = {
            title: response.data.title || '',
            description: response.data.description || '',
            file_path: response.data.file_path || ''
          };
        }
        
        console.log('Updated content:', this.content);
      } catch (error) {
        console.error('Ошибка при получении контента:', error);
      }
    },
    openDocument() {
      const documentUrl = this.content.file_path; // Предполагаем, что file_path содержит URL документа
      console.log('Opening document URL:', documentUrl); // Логируем URL
      if (documentUrl) {
        window.open(documentUrl, '_blank'); // Открывает документ в новой вкладке
      } else {
        console.error('Document URL is not valid:', documentUrl); // Логируем ошибку, если URL не валиден
      }
    },
    // http://192.168.81.149:8000 
    getDownloadLink(contentId) {
      return `${import.meta.env.VITE_API_URL}/download-file/${contentId}`;
    }
  }
};
</script>

<style scoped>
.card {
  margin: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.card-body {
  padding: 20px;
}

</style>