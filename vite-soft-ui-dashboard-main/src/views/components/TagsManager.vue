<template>
  <div class="card">
    <div class="card-header pb-0">
      <div class="row">
        <div class="col-lg-6 col-7">
          <h6>Управление тегами</h6>

        </div>
      </div>
    </div>
    <div class="card-body px-0 pb-2">
      <!-- Форма создания нового тега -->
      <div class="container mb-4">
        <div class="row">
          <div class="col-md-6">
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                placeholder="Название нового тега" 
                v-model="newTagName"
              >
              <button 
                class="btn btn-info" 
                type="button" 
                @click="createTag"
                :disabled="!newTagName.trim()"
              >
                Создать тег
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Список тегов -->
      <div class="table-responsive">
        <table class="table align-items-center mb-0">
          <thead>
            <tr>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
              №
              </th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                Название тега
              </th>
              <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Действия
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tag in tags" :key="tag.id">
              <td>
                <div class="d-flex px-2 py-1">
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">{{ tag.id }}</h6>
                  </div>
                </div>
              </td>
              <td>
                <div v-if="editingTagId === tag.id" class="input-group">
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="editTagName" 
                    @keyup.enter="updateTag"
                  >
                  <button class="btn btn-sm btn-info" @click="updateTag" style="background-color: #172d76;">
                    <i class="fas fa-save"></i>
                  </button>
                  <button class="btn btn-sm btn-secondary" @click="cancelEdit">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <p v-else class="text-xs font-weight-bold mb-0">{{ tag.tag_name }}</p>
              </td>
              <td class="align-middle text-center">
                <button 
                  v-if="editingTagId !== tag.id" 
                  @click="startEdit(tag)" 
                  class="btn btn-sm btn-info me-1"
                  style="background-color: #172d76;"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  @click="deleteTag(tag.id)" 
                  class="btn btn-sm btn-danger"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
            <tr v-if="tags.length === 0">
              <td colspan="3" class="text-center py-3">
                Нет доступных тегов
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Сообщения об операциях -->
      <div class="container mt-3" v-if="message">
        <div class="row">
          <div class="col-12">
            <div :class="['alert', status ? 'alert-success' : 'alert-danger']">
              {{ message }}
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
  name: "TagsManager",
  data() {
    return {
      tags: [],
      newTagName: '',
      editingTagId: null,
      editTagName: '',
      message: '',
      status: false
    };
  },
  mounted() {
    this.fetchTags();
  },
  methods: {
    async fetchTags() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/tags`);
        this.tags = response.data.tags;
      } catch (error) {
        console.error('Ошибка при получении тегов:', error);
        this.showMessage('Ошибка при получении тегов', false);
      }
    },
    async createTag() {
      if (!this.newTagName.trim()) return;
      
      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/content/create-tag`, null, {
          params: { tag_name: this.newTagName }
        });
        this.showMessage('Тег успешно создан', true);
        this.newTagName = '';
        this.fetchTags();
      } catch (error) {
        console.error('Ошибка при создании тега:', error);
        this.showMessage('Ошибка при создании тега', false);
      }
    },
    startEdit(tag) {
      this.editingTagId = tag.id;
      this.editTagName = tag.tag_name;
    },
    cancelEdit() {
      this.editingTagId = null;
      this.editTagName = '';
    },
    async updateTag() {
      if (!this.editTagName.trim() || !this.editingTagId) return;
      
      try {
        await axios.put(`${import.meta.env.VITE_API_URL}/content/update-tag/${this.editingTagId}`, null, {
          params: { tag_name: this.editTagName }
        });
        this.showMessage('Тег успешно обновлен', true);
        this.editingTagId = null;
        this.editTagName = '';
        this.fetchTags();
      } catch (error) {
        console.error('Ошибка при обновлении тега:', error);
        this.showMessage('Ошибка при обновлении тега', false);
      }
    },
    async deleteTag(tagId) {
      if (!confirm('Вы уверены, что хотите удалить этот тег?')) return;
      
      try {
        await axios.delete(`${import.meta.env.VITE_API_URL}/content/delete-tag/${tagId}`);
        this.showMessage('Тег успешно удален', true);
        this.fetchTags();
      } catch (error) {
        console.error('Ошибка при удалении тега:', error);
        this.showMessage('Ошибка при удалении тега', false);
      }
    },
    showMessage(text, isSuccess) {
      this.message = text;
      this.status = isSuccess;
      setTimeout(() => {
        this.message = '';
      }, 3000);
    }
  }
};
</script> 
<style>
.btn-info {
  background-color: #172d76;
  border-color: #7b7b7b;
  &:disabled {
    background-color: #344785;
    color: #ffffff;
  }
}
</style>