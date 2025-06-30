<template>
  <div class="card">
    <!-- <div class="card-header pb-0">
      <div class="row">
        <div class="col-lg-6 col-7">
        </div>
      </div>
    </div> -->
    <div class="card-body">
      <!-- Вкладки -->
      <ul class="nav nav-tabs" id="contentTabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link active" 
            id="edit-content-tab" 
            data-bs-toggle="tab" 
            data-bs-target="#edit-content" 
            type="button" 
            role="tab" 
            aria-controls="edit-content" 
            aria-selected="true"
            style="color: gray;"
          >
            Редактирование контента
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button 
            class="nav-link" 
            id="manage-tags-tab" 
            data-bs-toggle="tab" 
            data-bs-target="#manage-tags" 
            type="button" 
            role="tab" 
            aria-controls="manage-tags" 
            aria-selected="false"
             style="color: gray;"
          >
            Управление тегами
          </button>
        </li>
      </ul>

      <!-- Содержимое вкладок -->
      <div class="tab-content" id="contentTabsContent">
        <!-- Вкладка редактирования контента -->
        <div 
          class="tab-pane fade show active" 
          id="edit-content" 
          role="tabpanel" 
          aria-labelledby="edit-content-tab"
        >
          <div class="row mb-4 mt-4">
            <div class="col-12">
              <div class="form-group ">
                <label for="content-select" class="form-label">Выберите контент для редактирования</label>
                <select class="form-select" id="content-select" v-model="editForm.id" @change="loadContentForEdit">
                  <option value="">Выберите контент</option>
                  <option v-for="content in contentList" :key="content.id" :value="content.id">
                    {{ content.title }}
                  </option>
                </select>
              </div>
            </div>
          </div>
          
          <form @submit.prevent="editContent" v-if="editForm.id">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="edit-title" class="form-label">Название</label>
                <input type="text" class="form-control" id="edit-title" v-model="editForm.title" required>
              </div>
              <div class="col-md-6 mb-3">
                <label for="edit-description" class="form-label">Описание</label>
                <textarea class="form-control" id="edit-description" rows="3" v-model="editForm.description" required></textarea>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="edit-department" class="form-label">Отдел</label>
                <select class="form-select" id="edit-department" v-model="editForm.department_id" required>
                  <option v-for="department in departments" :key="department.id" :value="department.id">
                    {{ department.department_name }}
                  </option>
                </select>
              </div>
              <div class="col-md-6 mb-3">
                <label for="edit-access_level" class="form-label">Уровень доступа</label>
                <select class="form-select" id="edit-access_level" v-model="editForm.access_level" required>
                  <option v-for="access in accessLevels" :key="access.id" :value="access.id">
                    {{ access.access_name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="edit-tag" class="form-label">Тег</label>
                <select class="form-select" id="edit-tag" v-model="editForm.tag_id">
                  <option value="">Без категории</option>
                  <option v-for="tag in tags" :key="tag.id" :value="tag.id">
                    {{ tag.tag_name }}
                  </option>
                </select>
              </div>
            </div>
            <button type="submit" class="btn btn-info" style="background-color: #172d76; border-color: #172d76;">Сохранить изменения</button>
            <div v-if="editMessage" :class="['alert', editStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
              {{ editMessage }}
            </div>
          </form>
          <div v-else class="alert alert-info mt-4">
            Выберите контент для редактирования
          </div>
        </div>
        
        <!-- Вкладка управления тегами -->
        <div 
          class="tab-pane fade" 
          id="manage-tags" 
          role="tabpanel" 
          aria-labelledby="manage-tags-tab"
        >
          <TagsManager ref="tagsManager" @tags-updated="updateTags" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TagsManager from './TagsManager.vue';

export default {
  name: "ContentEditor",
  components: {
    TagsManager
  },
  props: {
    contentList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      editForm: {
        id: '',
        title: '',
        description: '',
        access_level: '',
        department_id: '',
        tag_id: ''
      },
      departments: [],
      accessLevels: [],
      tags: [],
      editMessage: '',
      editStatus: false
    };
  },
  mounted() {
    this.fetchDepartments();
    this.fetchAccessLevels();
    this.fetchTags();
  },
  methods: {
    async fetchDepartments() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/departments`);
        this.departments = response.data;
      } catch (error) {
        console.error('Ошибка при получении отделов:', error);
      }
    },
    async fetchAccessLevels() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/access-levels`);
        this.accessLevels = response.data;
      } catch (error) {
        console.error('Ошибка при получении уровней доступа:', error);
      }
    },
    async fetchTags() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/tags`);
        this.tags = response.data.tags;
      } catch (error) {
        console.error('Ошибка при получении тегов:', error);
      }
    },
    loadContentForEdit() {
      if (!this.editForm.id) {
        this.resetForm();
        return;
      }
      
      const content = this.contentList.find(c => c.id === this.editForm.id);
      if (content) {
        this.editForm = {
          id: content.id,
          title: content.title,
          description: content.description,
          access_level: content.access_level,
          department_id: content.department_id,
          tag_id: content.tag_id || ''
        };
      }
    },
    resetForm() {
      this.editForm = {
        id: '',
        title: '',
        description: '',
        access_level: '',
        department_id: '',
        tag_id: ''
      };
    },
    async editContent() {
      try {
        const response = await axios.put(`${import.meta.env.VITE_API_URL}/content/${this.editForm.id}`, this.editForm);
        this.editMessage = 'Контент успешно обновлен';
        this.editStatus = true;
        this.$emit('content-updated');
      } catch (error) {
        this.editMessage = error.response?.data?.detail || 'Ошибка при обновлении контента';
        this.editStatus = false;
        console.error('Ошибка при обновлении контента:', error);
      }
      
      setTimeout(() => {
        this.editMessage = '';
      }, 3000);
    },
    updateTags() {
      this.fetchTags();
    }
  }
};
</script> 

<style >
  .btn-info {
  background-color: #172d76;
  border-color: #7b7b7b;
  &:hover {
    background-color: #344785;
    border-color: #7b7b7b;
  }
}

.form-control:focus {
  border-color: #5e72e4;
  box-shadow: 0 0 0 0.2rem rgba(94, 114, 228, 0.25);
}
</style>