<template>
  <div class="card mb-4">
    <div class="card-header pb-0">
      <h6>Таблица контента</h6>
    </div>
    <div class="card-body px-0 pt-0 pb-2">
      <div class="table-responsive p-0">
        <table class="table align-items-center mb-0">
          <thead>
            <tr>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Название</th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Описание</th>
              <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Отдел</th>
              <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Уровень доступа</th>
              <th class="text-secondary opacity-7"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="content in contents" :key="content.id">
              <td>
                <div class="d-flex px-2 py-1">
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">{{ content.title }}</h6>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-xs text-secondary mb-0">{{ content.description }}</p>
              </td>
              <td class="align-middle text-center text-sm">
                <p class="text-xs font-weight-bold mb-0">{{ content.department_name }}</p>
              </td>
              <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold">{{ content.access_name }}</span>
              </td>
              <td class="align-middle text-center">
                <a
                  :href="getDownloadLink(content.id)"
                  class="text-secondary font-weight-bold text-xs"
                  data-toggle="tooltip"
                  data-original-title="Скачать файл"
                >Скачать</a>
              </td>
            </tr>
            <tr v-if="contents.length === 0">
              <td colspan="5" class="text-center py-4">
                <p class="text-secondary mb-0">Контент не найден</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "ContentTable",
  data() {
    return {
      contents: []
    };
  },
  async created() {
    await this.fetchAllContent();
  },
  methods: {
    // Получение всего контента
    async fetchAllContent() {
      try {
        const userId = localStorage.getItem("userId");
        if (!userId) {
          return;
        }
        
        // Получаем данные о пользователе
        const userResponse = await axios.get(`http://localhost:8000/user/${userId}`);
        const user = userResponse.data;
        
        // Получаем контент для пользователя
        const response = await axios.get(`http://localhost:8000/user/${userId}/content`);
        this.contents = response.data;
      } catch (error) {
        this.contents = [];
      }
    },
    
    // Получение ссылки для скачивания файла
    getDownloadLink(contentId) {
      return `${import.meta.env.VITE_API_URL}/download-file/${contentId}`;
    }
  }
};
</script>

<style scoped>
.table th, .table td {
  padding: 12px;
}

.table th {
  font-size: 0.65rem;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}
</style> 