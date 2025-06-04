<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messagesContainer">
      <div v-if="chatHistory.length === 0" class="empty-chat">
        <h3>Начните диалог с вашим Local LLM</h3>
        <p>Задайте вопрос о ваших документах</p>
      </div>
      
      <div v-for="(message, index) in chatHistory" :key="index" class="message-container">
        <div class="user-message">
          <div class="avatar user">
            <i class="fas fa-user"></i>
          </div>
          <div class="message">{{ message.user }}</div>
        </div>
        
        <div class="assistant-message">
          <div class="avatar assistant">
            <i class="fas fa-robot"></i>
          </div>
          <div class="message">
            <div v-html="formatMessage(message.assistant)"></div>
            
            <div v-if="message.chunks && message.chunks.length > 0" class="sources-container">
              <h6 @click="toggleSources(index)" class="sources-toggle">
                <i :class="['fas', showSources[index] ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                Источники ({{ message.files.length }})
              </h6>
              
              <div v-if="showSources[index]" class="sources-list">
                <div v-for="(file, fileIndex) in message.files" :key="fileIndex" class="source-item">
                  <i class="fas fa-file-alt"></i> {{ file }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="isLoading" class="loading-message">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Загрузка...</span>
        </div>
        Обработка запроса...
      </div>
    </div>
    
    <div class="chat-input">
      <form @submit.prevent="sendMessage">
        <div class="input-group">
          <textarea 
            v-model="userInput" 
            class="form-control" 
            placeholder="Введите ваш вопрос..."
            rows="2"
            @keydown.enter.prevent="sendMessage"
          ></textarea>
          <button 
            type="submit" 
            class="btn btn-primary" 
            :disabled="isLoading || !userInput.trim()"
          >
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export default {
  name: 'ChatInterface',
  data() {
    return {
      userInput: '',
      showSources: {}
    };
  },
  computed: {
    ...mapState(['chatHistory', 'isLoading', 'error'])
  },
  methods: {
    ...mapActions(['sendQuery']),
    
    async sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return;
      
      const question = this.userInput.trim();
      this.userInput = '';
      
      try {
        await this.sendQuery(question);
      } catch (error) {
        console.error('Error sending message:', error);
      }
      
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
    
    formatMessage(message) {
      // Преобразование Markdown в HTML и очистка
      return DOMPurify.sanitize(marked(message));
    },
    
    toggleSources(index) {
      this.$set(this.showSources, index, !this.showSources[index]);
    },
    
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      container.scrollTop = container.scrollHeight;
    }
  },
  updated() {
    this.scrollToBottom();
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: calc(100vh - 120px);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #f8f9fa;
}

.empty-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  opacity: 0.7;
}

.message-container {
  margin-bottom: 1.5rem;
}

.user-message,
.assistant-message {
  display: flex;
  margin-bottom: 0.5rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.avatar.user {
  background-color: #007bff;
  color: white;
}

.avatar.assistant {
  background-color: #28a745;
  color: white;
}

.message {
  background-color: white;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  max-width: calc(100% - 60px);
}

.user-message .message {
  background-color: #e9f5ff;
}

.sources-container {
  margin-top: 0.75rem;
  border-top: 1px solid #eee;
  padding-top: 0.5rem;
}

.sources-toggle {
  cursor: pointer;
  font-size: 0.9rem;
  color: #6c757d;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.sources-list {
  margin-top: 0.5rem;
  font-size: 0.85rem;
}

.source-item {
  margin: 0.25rem 0;
  padding: 0.25rem 0.5rem;
  background-color: #f5f5f5;
  border-radius: 0.25rem;
}

.chat-input {
  padding: 1rem;
  border-top: 1px solid #e9ecef;
  background-color: white;
}

.loading-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  font-style: italic;
  color: #6c757d;
}
</style>
