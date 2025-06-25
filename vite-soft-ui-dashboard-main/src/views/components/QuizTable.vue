<template>

    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <div class="d-flex justify-content-between align-items-center">
              <h6>Тестирование и анкетирование</h6>
              <div>
                <button class="btn btn-sm btn-primary me-2" style="" @click="showQuizzes(true)">
                  Тесты
                </button>
                <button class="btn btn-sm btn-info" @click="showQuizzes(false)">
                  Анкеты
                </button>
              </div>
            </div>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <!-- Загрузка данных -->
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
              </div>
              <p class="mt-2">Загрузка данных...</p>
            </div>

            <!-- Сообщение об ошибке -->
            <div v-else-if="error" class="alert alert-danger m-3">
              {{ error }}
            </div>

            <!-- Таблица с тестами/анкетами -->
            <div v-else class="table-responsive p-0">
              <table class="table align-items-center mb-0">
                <thead>
                  <tr>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Название</th>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Описание</th>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Вопросов</th>
                    <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">Дата создания</th>
                    <th class="text-secondary opacity-7"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                    <td>
                      <div class="d-flex px-2 py-1">
                        <div>
                          <i class="fas me-3" :class="quiz.is_test ? 'fa-clipboard-check text-primary' : 'fa-clipboard-list text-info'"></i>
                        </div>
                        <div class="d-flex flex-column justify-content-center">
                          <h6 class="mb-0 text-sm">{{ quiz.title }}</h6>
                        </div>
                      </div>
                    </td>
                    <td>
                      <p class="text-xs text-secondary mb-0">{{ quiz.description || 'Нет описания' }}</p>
                    </td>
                    <td>
                      <span class="badge bg-gradient-success">{{ quiz.question_count }}</span>
                    </td>
                    <td>
                      <span class="text-secondary text-xs font-weight-bold">{{ formatDate(quiz.created_at) }}</span>
                    </td>
                    <td class="align-middle">
                      <button class="btn btn-sm btn-success me-2" @click="startQuiz(quiz)">
                        <i class="fas fa-play me-1"></i> Пройти
                      </button>
                      <button v-if="quiz.is_test" class="btn btn-sm btn-info" @click="viewResults(quiz)">
                        <i class="fas fa-chart-bar me-1"></i> Результаты
                      </button>
                    </td>
                  </tr>
                  <tr v-if="filteredQuizzes.length === 0">
                    <td colspan="5" class="text-center py-4">
                      {{ showTestsOnly ? 'Тестов не найдено' : 'Анкет не найдено' }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно для прохождения теста/анкеты -->
    <div class="modal fade" id="quizModal" tabindex="-1" aria-labelledby="quizModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="quizModalLabel">{{ currentQuiz ? currentQuiz.title : '' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="quizLoading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
              </div>
              <p class="mt-2">Загрузка теста...</p>
            </div>
            <div v-else-if="quizError" class="alert alert-danger">
              {{ quizError }}
            </div>
            <div v-else-if="currentQuiz && currentQuiz.questions">
              <p class="mb-4">{{ currentQuiz.description }}</p>
              
              <form @submit.prevent="submitQuiz">
                <div v-for="(question, index) in currentQuiz.questions" :key="question.id" class="mb-4 p-3 border rounded">
                  <h6 class="mb-3">{{ index + 1 }}. {{ question.text }}</h6>
                  
                  <!-- Вопрос с одиночным выбором -->
                  <div v-if="question.question_type === 'single_choice'" class="ms-3">
                    <div v-for="option in question.options" :key="option.id" class="form-check mb-2">
                      <input 
                        :id="`question-${question.id}-option-${option.id}`" 
                        class="form-check-input" 
                        type="radio" 
                        :name="`question-${question.id}`" 
                        :value="option.id"
                        v-model="answers[question.id]"
                      >
                      <label class="form-check-label" :for="`question-${question.id}-option-${option.id}`">
                        {{ option.text }}
                      </label>
                    </div>
                  </div>
                  
                  <!-- Вопрос с множественным выбором -->
                  <div v-else-if="question.question_type === 'multiple_choice'" class="ms-3">
                    <div v-for="option in question.options" :key="option.id" class="form-check mb-2">
                      <input 
                        :id="`question-${question.id}-option-${option.id}`" 
                        class="form-check-input" 
                        type="checkbox" 
                        :value="option.id"
                        v-model="answers[question.id]"
                      >
                      <label class="form-check-label" :for="`question-${question.id}-option-${option.id}`">
                        {{ option.text }}
                      </label>
                    </div>
                  </div>
                  
                  <!-- Вопрос с текстовым ответом -->
                  <div v-else-if="question.question_type === 'text'" class="ms-3">
                    <div class="mb-3">
                      <input 
                        type="text" 
                        class="form-control" 
                        :id="`question-${question.id}`"
                        v-model="answers[question.id]"
                        placeholder="Введите ваш ответ"
                      >
                    </div>
                  </div>
                </div>
                
                <div class="d-grid gap-2">
                  <button type="submit" class="btn btn-primary">Отправить ответы</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Модальное окно для просмотра результатов -->
    <div class="modal fade" id="resultsModal" tabindex="-1" aria-labelledby="resultsModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="resultsModalLabel">Результаты: {{ currentQuiz ? currentQuiz.title : '' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="resultsLoading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
              </div>
              <p class="mt-2">Загрузка результатов...</p>
            </div>
            <div v-else-if="resultsError" class="alert alert-danger">
              {{ resultsError }}
            </div>
            <div v-else-if="userAttempts && userAttempts.length > 0">
              <h6 class="mb-3">Ваши попытки:</h6>
              <div class="table-responsive">
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th>Дата</th>
                      <th>Результат</th>
                      <th>Действия</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="attempt in userAttempts" :key="attempt.id">
                      <td>{{ formatDate(attempt.completed_at || attempt.started_at) }}</td>
                      <td>
                        <span v-if="attempt.score !== null">
                          {{ attempt.score }} / {{ attempt.total_questions }}
                          ({{ Math.round(attempt.score / attempt.total_questions * 100) }}%)
                        </span>
                        <span v-else>-</span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-info" @click="viewAttemptDetails(attempt)">
                          Подробнее
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <div v-if="selectedAttempt" class="mt-4">
                <h6 class="mb-3">Детали попытки от {{ formatDate(selectedAttempt.completed_at || selectedAttempt.started_at) }}:</h6>
                <div class="list-group">
                  <div v-for="answer in selectedAttempt.answers" :key="answer.id" class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1">Вопрос: {{ getQuestionText(answer.question_id) }}</h6>
                      <small v-if="answer.is_correct !== null" :class="answer.is_correct ? 'text-success' : 'text-danger'">
                        {{ answer.is_correct ? 'Верно' : 'Неверно' }}
                      </small>
                    </div>
                    <p class="mb-1">Ваш ответ: {{ formatAnswer(answer) }}</p>
                    <small v-if="answer.is_correct === false" class="text-muted">
                      Правильный ответ: {{ getCorrectAnswer(answer.question_id) }}
                    </small>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="alert alert-info">
              У вас еще нет попыток прохождения этого теста.
            </div>
          </div>
        </div>
      </div>
    </div>

</template>

<script>
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  name: "QuizTable",
  data() {
    return {
      userId: localStorage.getItem("userId"),
      quizzes: [],
      loading: true,
      error: null,
      showTestsOnly: true,
      
      // Данные для модального окна с тестом
      quizModal: null,
      currentQuiz: null,
      quizLoading: false,
      quizError: null,
      answers: {},
      
      // Данные для модального окна с результатами
      resultsModal: null,
      userAttempts: [],
      resultsLoading: false,
      resultsError: null,
      selectedAttempt: null
    };
  },
  computed: {
    filteredQuizzes() {
      return this.quizzes.filter(quiz => quiz.is_test === this.showTestsOnly);
    }
  },
  async created() {
    if (!this.userId) {
      this.$router.push("/sign-in");
      return;
    }
    
    await this.fetchQuizzes();
  },
  mounted() {
    // Инициализируем модальные окна
    this.quizModal = new Modal(document.getElementById('quizModal'));
    this.resultsModal = new Modal(document.getElementById('resultsModal'));
    
    // Обработчик закрытия модального окна с тестом
    document.getElementById('quizModal').addEventListener('hidden.bs.modal', () => {
      this.answers = {};
    });
  },
  methods: {
    async fetchQuizzes() {
      try {
        this.loading = true;
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/list?user_id=${this.userId}`);
        this.quizzes = response.data;
        this.loading = false;
      } catch (error) {
        console.error("Ошибка при получении тестов и анкет:", error);
        this.error = "Произошла ошибка при загрузке тестов и анкет";
        this.loading = false;
      }
    },
    
    showQuizzes(isTest) {
      this.showTestsOnly = isTest;
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('ru-RU', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    async startQuiz(quiz) {
      try {
        this.quizLoading = true;
        this.currentQuiz = null;
        this.quizError = null;
        this.answers = {};
        
        // Открываем модальное окно
        this.quizModal.show();
        
        // Получаем детали теста/анкеты
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/${quiz.id}?user_id=${this.userId}`);
        this.currentQuiz = response.data;
        
        // Инициализируем ответы
        this.currentQuiz.questions.forEach(question => {
          if (question.question_type === 'multiple_choice') {
            this.answers[question.id] = [];
          } else {
            this.answers[question.id] = '';
          }
        });
        
        this.quizLoading = false;
      } catch (error) {
        console.error("Ошибка при загрузке теста:", error);
        this.quizError = "Произошла ошибка при загрузке теста";
        this.quizLoading = false;
      }
    },
    
    async submitQuiz() {
      try {
        // Преобразуем ответы в формат для API
        const formattedAnswers = [];
        for (const [questionId, answer] of Object.entries(this.answers)) {
          formattedAnswers.push({
            question_id: parseInt(questionId),
            answer: answer
          });
        }
        
        // Отправляем ответы
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/quiz/attempt`, {
          quiz_id: this.currentQuiz.id,
          answers: formattedAnswers
        }, {
          params: {
            user_id: this.userId
          }
        });
        
        // Закрываем модальное окно
        this.quizModal.hide();
        
        // Показываем сообщение об успешном прохождении
        alert(this.currentQuiz.is_test ? 
          `Тест успешно пройден! Ваш результат: ${response.data.score} баллов.` : 
          'Анкета успешно отправлена!');
        
        // Если это тест, предлагаем посмотреть результаты
        if (this.currentQuiz.is_test) {
          this.viewResults(this.currentQuiz);
        }
      } catch (error) {
        console.error("Ошибка при отправке ответов:", error);
        alert("Произошла ошибка при отправке ответов. Пожалуйста, попробуйте еще раз.");
      }
    },
    
    async viewResults(quiz) {
      try {
        this.resultsLoading = true;
        this.currentQuiz = quiz;
        this.userAttempts = [];
        this.resultsError = null;
        this.selectedAttempt = null;
        
        // Открываем модальное окно
        this.resultsModal.show();
        
        // Получаем попытки пользователя
        const attemptsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/attempts/${this.userId}?quiz_id=${quiz.id}`);
        this.userAttempts = attemptsResponse.data;
        
        // Получаем детали теста для отображения вопросов
        const quizResponse = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/${quiz.id}?user_id=${this.userId}`);
        this.currentQuiz = quizResponse.data;
        
        this.resultsLoading = false;
        
        // Если есть попытки, показываем детали последней
        if (this.userAttempts.length > 0) {
          this.viewAttemptDetails(this.userAttempts[0]);
        }
      } catch (error) {
        console.error("Ошибка при загрузке результатов:", error);
        this.resultsError = "Произошла ошибка при загрузке результатов";
        this.resultsLoading = false;
      }
    },
    
    async viewAttemptDetails(attempt) {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/attempt/${attempt.id}?user_id=${this.userId}`);
        this.selectedAttempt = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке деталей попытки:", error);
        alert("Произошла ошибка при загрузке деталей попытки");
      }
    },
    
    getQuestionText(questionId) {
      if (!this.currentQuiz || !this.currentQuiz.questions) return '';
      const question = this.currentQuiz.questions.find(q => q.id === questionId);
      return question ? question.text : '';
    },
    
    getCorrectAnswer(questionId) {
      if (!this.currentQuiz || !this.currentQuiz.questions) return '';
      const question = this.currentQuiz.questions.find(q => q.id === questionId);
      if (!question || !question.correct_answer) return '';
      
      if (question.question_type === 'single_choice') {
        const option = question.options.find(o => o.id === question.correct_answer);
        return option ? option.text : '';
      } else if (question.question_type === 'multiple_choice') {
        const selectedOptions = question.options.filter(o => question.correct_answer.includes(o.id));
        return selectedOptions.map(o => o.text).join(', ');
      } else {
        return question.correct_answer;
      }
    },
    
    formatAnswer(answer) {
      if (!answer || !answer.answer) return '-';
      
      const question = this.currentQuiz.questions.find(q => q.id === answer.question_id);
      if (!question) return JSON.stringify(answer.answer);
      
      if (question.question_type === 'single_choice') {
        const option = question.options.find(o => o.id === answer.answer);
        return option ? option.text : answer.answer;
      } else if (question.question_type === 'multiple_choice') {
        const selectedOptions = question.options.filter(o => answer.answer.includes(o.id));
        return selectedOptions.map(o => o.text).join(', ');
      } else {
        return answer.answer;
      }
    }
  }
};
</script>

<style scoped>
.form-check-input:checked {
  background-color: #5e72e4;
  border-color: #5e72e4;
}
</style>
