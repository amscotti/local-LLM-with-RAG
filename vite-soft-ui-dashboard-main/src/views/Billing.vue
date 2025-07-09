<template>
  <div class="container-fluid mt-4">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>Чат с LLM</h6>
          </div>
          <div class="card-body">
            <div class="mb-4">
              <label class="form-label">Режим чата</label>
              <div class="form-check">
                <input class="form-check-input" type="radio" name="chatMode" id="modeRAG" value="rag" v-model="chatMode">
                <label class="form-check-label" for="modeRAG">
                  С базой знаний (RAG)
                </label>
              </div>
              <div class="form-check">
                <input class="form-check-input" type="radio" name="chatMode" id="modeSimple" value="simple" v-model="chatMode">
                <label class="form-check-label" for="modeSimple">
                  Простой чат
                </label>
              </div>
            </div>
            
            <!-- Чат -->
            <div class="chat-container mb-4" style="height: 400px; overflow-y: auto; border: 1px solid #eee; border-radius: 10px; padding: 15px;">
              <div v-for="(message, index) in chatMessages" :key="index" class="mb-3">
                <div :class="message.role === 'user' ? 'text-end' : 'text-start'">
                  <div 
                    :class="[
                      'p-3 rounded d-inline-block', 
                      message.role === 'user' 
                        ? 'bg-gradient-info text-white' 
                        : 'bg-gray-100'
                    ]"
                    style="max-width: 80%"
                  >
                    <div v-html="formatMessage(message.content)"></div>
                  </div>
                </div>
              </div>
              <div v-if="isLoading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Загрузка...</span>
                </div>
              </div>
            </div>
            
            <!-- Форма ввода -->
            <div class="row">
              <div class="col">
                <div class="form-group">
                  <div class="input-group">
                    <input 
                      type="text" 
                      class="form-control" 
                      placeholder="Введите ваш вопрос..." 
                      v-model="userMessage"
                      @keyup.enter="sendMessage"
                      :disabled="isLoading"
                    >
                    <button 
                      class="btn btn-info mb-0" 
                      style="background-color: #173376; border-color: #7b7b7b; color: #fff;"
                      @click="sendMessage"
                      :disabled="isLoading || !userMessage.trim()"
                    >
                      <i class="fas fa-paper-plane"></i>
                    </button>
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
  name: "BillingPage",
  data() {
    return {
      userMessage: "",
      chatMessages: [],
      isLoading: false,
      chatMode: "rag", // По умолчанию используем режим с RAG
      requestInProgress: false, // Флаг для отслеживания текущего запроса
      requestTimeout: null, // Таймер для отмены запроса
      lastRequestTime: 0 // Время последнего запроса
    };
  },
  methods: {
    formatMessage(text) {
      if (!text) return '';
      // Заменяем \n на <br> для сохранения переносов строк
      return text.replace(/\n/g, '<br>');
    },
    async sendMessage() {
      if (!this.userMessage.trim()) return;
      
      // Защита от слишком частых запросов
      const now = Date.now();
      if (now - this.lastRequestTime < 1000) { // Минимальный интервал между запросами - 1 секунда
        console.warn("Запросы отправляются слишком часто. Пожалуйста, подождите.");
        return;
      }
      
      // Защита от повторных запросов
      if (this.requestInProgress) {
        console.warn("Предыдущий запрос еще обрабатывается. Пожалуйста, подождите.");
        return;
      }
      
      this.lastRequestTime = now;
      this.requestInProgress = true;
      
      const userId = localStorage.getItem("userId");
      const departmentId = localStorage.getItem("departmentId");
      const isAuthenticated = localStorage.getItem("isAuthenticated");
      
      if (!isAuthenticated || isAuthenticated !== "true") {
        console.error("Пользователь не аутентифицирован.");
        this.requestInProgress = false;
        return; // Прекращаем выполнение, если пользователь не аутентифицирован
      }
      
      if (!departmentId) {
        console.error("department_id не найден. Убедитесь, что пользователь вошел в систему.");
        this.requestInProgress = false;
        return; // Прекращаем выполнение, если departmentId отсутствует
      }
      
      console.log("Отправляемые данные:", {
        question: this.userMessage,
        department_id: departmentId
      });
      
      // Добавляем сообщение пользователя в чат
      this.chatMessages.push({
        role: 'user',
        content: this.userMessage
      });
      
      const message = this.userMessage;
      this.userMessage = "";
      this.isLoading = true;
      
      // Устанавливаем таймаут для запроса (2 минуты)
      this.requestTimeout = setTimeout(() => {
        if (this.isLoading) {
          this.isLoading = false;
          this.requestInProgress = false;
          this.chatMessages.push({
            role: 'assistant',
            content: '⏱️ Обработка запроса занимает больше времени, чем ожидалось. Запрос продолжает обрабатываться на сервере, ответ может прийти позже.'
          });
        }
      }, 120000);
      
      try {
        let response;
        
        if (this.chatMode === "rag") {
          // Создаем задачу для обработки в режиме с RAG (новый асинхронный API)
          const taskResponse = await axios.post(`${import.meta.env.VITE_API_URL}/llm/query`, { 
            question: message,
            department_id: departmentId
          }, {
            noRetry: true
          });
          
          const taskId = taskResponse.data.task_id;
          console.log(`Создана задача: ${taskId}`);
          
          // Добавляем временное сообщение о статусе
          const processingMessageIndex = this.chatMessages.length;
          this.chatMessages.push({
            role: 'assistant',
            content: '🔄 Обрабатываю ваш запрос...',
            isProcessing: true
          });
          
          // Опрашиваем статус задачи до завершения
          let maxAttempts = 60; // Максимум 60 попыток (2 минуты)
          let attempts = 0;
          
          while (attempts < maxAttempts) {
            attempts++;
            
            try {
              const resultResponse = await axios.get(`${import.meta.env.VITE_API_URL}/llm/query/${taskId}`);
              const taskResult = resultResponse.data;
              
              if (taskResult.status === 'completed') {
                // Задача завершена успешно
                this.chatMessages[processingMessageIndex] = {
                  role: 'assistant',
                  content: taskResult.answer || 'Ответ получен, но содержимое пустое.',
                  isProcessing: false
                };
                break;
              } else if (taskResult.status === 'failed') {
                // Задача завершена с ошибкой
                this.chatMessages[processingMessageIndex] = {
                  role: 'assistant',
                  content: `❌ Произошла ошибка при обработке: ${taskResult.error || 'Неизвестная ошибка'}`,
                  isProcessing: false
                };
                break;
              } else if (taskResult.status === 'processing') {
                // Задача в обработке, обновляем сообщение
                this.chatMessages[processingMessageIndex].content = '⚙️ Запрос обрабатывается, пожалуйста подождите...';
              }
              
              // Ждем 2 секунды перед следующей попыткой
              await new Promise(resolve => setTimeout(resolve, 2000));
              
            } catch (pollError) {
              console.error("Ошибка при опросе статуса задачи:", pollError);
              
              // Если опрос статуса не удался несколько раз подряд
              if (attempts >= 3) {
                this.chatMessages[processingMessageIndex] = {
                  role: 'assistant',
                  content: `❌ Не удалось получить результат обработки. Попробуйте еще раз.`,
                  isProcessing: false
                };
                break;
              }
              
              await new Promise(resolve => setTimeout(resolve, 2000));
            }
          }
          
          // Если превышено максимальное количество попыток
          if (attempts >= maxAttempts) {
            this.chatMessages[processingMessageIndex] = {
              role: 'assistant',
              content: '⏱️ Обработка запроса занимает больше времени, чем ожидалось. Попробуйте позже.',
              isProcessing: false
            };
          }
        } else {
          // Используем эндпоинт /generate для простого чата
          response = await axios.post(`${import.meta.env.VITE_API_URL}/llm/generate`, {
            messages: message,
            department_id: departmentId // Добавляем department_id в запрос
          }, {
            // Отключаем автоматические повторные попытки для запросов к LLM
            noRetry: true
          });
          
          // Добавляем ответ в чат
          this.chatMessages.push({
            role: 'assistant',
            content: response.data.text
          });
        }
      } catch (error) {
        console.error("Ошибка при отправке сообщения:", error);
        
        // Добавляем сообщение об ошибке в чат
        this.chatMessages.push({
          role: 'assistant',
          content: `Произошла ошибка: ${error.response?.data?.detail || error.message || 'Неизвестная ошибка'}`
        });
      } finally {
        // Очищаем таймаут
        if (this.requestTimeout) {
          clearTimeout(this.requestTimeout);
          this.requestTimeout = null;
        }
        
        this.isLoading = false;
        this.requestInProgress = false;
        
        // Прокручиваем чат вниз
        this.$nextTick(() => {
          const chatContainer = document.querySelector('.chat-container');
          if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
          }
        });
      }
    }
  },
  mounted() {
    // Добавляем приветственное сообщение
    this.chatMessages.push({
      role: 'assistant',
      content: 'Здравствуйте! Я ваш ИИ-ассистент. Как я могу вам помочь сегодня?'
    });
  },
  created() {
    const isAuthenticated = localStorage.getItem("isAuthenticated");
    if (!isAuthenticated || isAuthenticated !== "true") {
      this.$router.push("/sign-in"); // Перенаправляем на страницу входа
    }
  }
};
</script>

<style scoped>
.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
