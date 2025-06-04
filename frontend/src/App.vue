<script>
import { mapState, mapMutations } from 'vuex';
import ChatInterface from '@/components/ChatInterface.vue';
import SettingsPanel from '@/components/SettingsPanel.vue';

export default {
  name: 'App',
  components: {
    ChatInterface,
    SettingsPanel
  },
  computed: {
    ...mapState(['error'])
  },
  methods: {
    ...mapMutations(['CLEAR_ERROR']),
    
    clearError() {
      this.CLEAR_ERROR();
    }
  }
};
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="container-fluid">
        <h1>Local LLM with RAG</h1>
      </div>
    </header>
    
    <main class="app-main">
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-9">
            <ChatInterface />
          </div>
          <div class="col-md-3">
            <SettingsPanel />
          </div>
        </div>
      </div>
    </main>
    
    <div v-if="error" class="error-notification">
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ error }}
        <button @click="clearError" type="button" class="btn-close"></button>
      </div>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  padding: 0;
}

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  background-color: #007bff;
  color: white;
  padding: 1rem;
}

.app-main {
  flex: 1;
  padding: 1rem;
}

.error-notification {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1rem;
}
</style>
