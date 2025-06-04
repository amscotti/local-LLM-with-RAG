import { createStore } from 'vuex';
import api from '@/services/api';

export default createStore({
  state: {
    chatHistory: [],
    isInitialized: false,
    currentModel: 'mistral',
    currentEmbeddingModel: 'nomic-embed-text',
    documentsPath: 'Research',
    isLoading: false,
    error: null
  },
  mutations: {
    ADD_MESSAGE(state, { user, assistant, chunks, files }) {
      state.chatHistory.push({ user, assistant, chunks, files, timestamp: new Date() });
    },
    SET_INITIALIZED(state, value) {
      state.isInitialized = value;
    },
    SET_MODELS(state, { model, embeddingModel, documentsPath }) {
      state.currentModel = model || state.currentModel;
      state.currentEmbeddingModel = embeddingModel || state.currentEmbeddingModel;
      state.documentsPath = documentsPath || state.documentsPath;
    },
    SET_LOADING(state, value) {
      state.isLoading = value;
    },
    SET_ERROR(state, error) {
      state.error = error;
    },
    CLEAR_ERROR(state) {
      state.error = null;
    }
  },
  actions: {
    async sendQuery({ commit, state }, question) {
      try {
        commit('SET_LOADING', true);
        commit('CLEAR_ERROR');
        
        if (!state.isInitialized) {
          await this.dispatch('initialize');
        }
        
        const response = await api.query(question, state.currentModel);
        
        commit('ADD_MESSAGE', {
          user: question,
          assistant: response.answer,
          chunks: response.chunks,
          files: response.files
        });
        
        return response;
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async initialize({ commit, state }) {
      try {
        commit('SET_LOADING', true);
        commit('CLEAR_ERROR');
        
        const response = await api.initialize(
          state.currentModel,
          state.currentEmbeddingModel,
          state.documentsPath
        );
        
        commit('SET_INITIALIZED', true);
        return response;
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    async uploadFile({ commit }, file) {
      try {
        commit('SET_LOADING', true);
        commit('CLEAR_ERROR');
        
        const response = await api.uploadFile(file);
        return response;
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message);
        throw error;
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    updateModels({ commit }, { model, embeddingModel, documentsPath }) {
      commit('SET_MODELS', { model, embeddingModel, documentsPath });
    }
  }
});
