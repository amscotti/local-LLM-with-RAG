<template>
  <div class="settings-panel">
    <h4>Настройки</h4>
    
    <div class="mb-3">
      <label class="form-label">Модель LLM</label>
      <select v-model="model" class="form-select">
        <option value="mistral">Mistral</option>
        <option value="llama3">Llama 3</option>
        <option value="ilyagusev/saiga_llama3">Saiga Llama 3</option>
      </select>
    </div>
    
    <div class="mb-3">
      <label class="form-label">Модель эмбеддингов</label>
      <select v-model="embeddingModel" class="form-select">
        <option value="nomic-embed-text">Nomic Embed Text</option>
        <option value="all-MiniLM-L6-v2">MiniLM L6</option>
      </select>
    </div>
    
    <div class="mb-3">
      <label class="form-label">Путь к документам</label>
      <input type="text" v-model="documentsPath" class="form-control" />
    </div>
    
    <div class="d-flex justify-content-between">
      <button 
        @click="applySettings" 
        class="btn btn-primary" 
        :disabled="isLoading"
      >
        Применить
      </button>
      
      <button 
        @click="initialize" 
        class="btn btn-outline-primary" 
        :disabled="isLoading"
      >
        Инициализировать
      </button>
    </div>
    
    <div class="mt-4">
      <h5>Загрузка документов</h5>
      <div class="mb-3">
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileChange" 
          class="form-control" 
        />
      </div>
      
      <button 
        @click="uploadFile" 
        class="btn btn-success" 
        :disabled="isLoading || !selectedFile"
      >
        Загрузить файл
      </button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'SettingsPanel',
  data() {
    return {
      model: '',
      embeddingModel: '',
      documentsPath: '',
      selectedFile: null
    };
  },
  computed: {
    ...mapState(['currentModel', 'currentEmbeddingModel', 'documentsPath', 'isInitialized', 'isLoading'])
  },
  created() {
    this.model = this.currentModel;
    this.embeddingModel = this.currentEmbeddingModel;
    this.documentsPath = this.documentsPath;
  },
  methods: {
    ...mapActions(['updateModels', 'initialize', 'uploadFile']),
    
    applySettings() {
      this.updateModels({
        model: this.model,
        embeddingModel: this.embeddingModel,
        documentsPath: this.documentsPath
      });
      
      this.$toast.success('Настройки применены');
    },
    
    async handleFileChange(event) {
      this.selectedFile = event.target.files[0] || null;
    },
    
    async uploadFile() {
      if (!this.selectedFile) return;
      
      try {
        await this.uploadFile(this.selectedFile);
        this.$toast.success('Файл успешно загружен');
        this.selectedFile = null;
        this.$refs.fileInput.value = '';
      } catch (error) {
        console.error('Error uploading file:', error);
        this.$toast.error('Ошибка при загрузке файла');
      }
    }
  }
};
</script>

<style scoped>
.settings-panel {
  padding: 1.5rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
</style>
