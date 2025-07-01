<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <authors-table ref="authorsTable" />
      </div>
    </div>
    
    <!-- Таблица контента -->
    <div class="row mt-4">
      <div class="col-12">
        <content-table ref="contentTable" />
      </div>
    </div>
    
    <!-- Админ-панель -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>Панель администратора</h6>
          </div>
          <div class="card-body">
            <ul class="nav nav-tabs" id="adminTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" id="register-tab" data-bs-toggle="tab" data-bs-target="#register" type="button" role="tab" aria-controls="register" aria-selected="true">Регистрация пользователей</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="upload-tab" data-bs-toggle="tab" data-bs-target="#upload" type="button" role="tab" aria-controls="upload" aria-selected="false">Загрузка контента</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link " id="initialize-tab" data-bs-toggle="tab" data-bs-target="#initialize" type="button" role="tab" aria-controls="initialize" aria-selected="false">Инициализация LLM</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="edit-tab" data-bs-toggle="tab" data-bs-target="#edit" type="button" role="tab" aria-controls="edit" aria-selected="false">Редактирование контента</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="feedback-tab" data-bs-toggle="tab" data-bs-target="#feedback" type="button" role="tab" aria-controls="feedback" aria-selected="false">Обратная связь</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="quiz-tab" data-bs-toggle="tab" data-bs-target="#quiz" type="button" role="tab" aria-controls="quiz" aria-selected="false">Тесты и анкеты</button>
              </li>
            </ul>
            
            <div class="tab-content mt-3" id="adminTabsContent">
              <!-- Вкладка регистрации пользователей -->
              <div class="tab-pane fade show active" id="register" role="tabpanel" aria-labelledby="register-tab">
                <form @submit.prevent="registerUser">
                  <div class="row">
                    <div class="col-md-4 mb-3">
                      <label for="login" class="form-label">Логин</label>
                      <input type="text" class="form-control" id="login" v-model="registerForm.login" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label for="password" class="form-label">Пароль</label>
                      <input type="password" class="form-control" id="password" v-model="registerForm.password" required>
                    </div>
                    <div class="col-md-4 mb-3">
                      <label for="role" class="form-label">Роль</label>
                      <select class="form-select" id="role" v-model="registerForm.role_id" required>
                        <option value="1">Администратор</option>
                        <option value="2">Пользователь</option>
                      </select>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="department" class="form-label">Отдел</label>
                      <select class="form-select" id="department" v-model="registerForm.department_id" required>
                        <option v-for="department in departments" :key="department.id" :value="department.id">
                          {{ department.department_name }}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="access" class="form-label">Уровень доступа</label>
                      <select class="form-select" id="access" v-model="registerForm.access_id" required>
                        <option v-for="access in accessLevels" :key="access.id" :value="access.id">
                          {{ access.access_name }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <button type="submit" class="btn btn-info">Зарегистрировать</button>
                  <div v-if="registerMessage" :class="['alert', registerStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
                    {{ registerMessage }}
                  </div>
                </form>
              </div>
              
              <!-- Вкладка загрузки контента -->
              <div class="tab-pane fade" id="upload" role="tabpanel" aria-labelledby="upload-tab">
                <form @submit.prevent="uploadContent">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="title" class="form-label">Название</label>
                      <input type="text" class="form-control" id="title" v-model="contentForm.title" required>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="description" class="form-label">Описание</label>
                      <textarea class="form-control" id="description" rows="3" v-model="contentForm.description"></textarea>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="department" class="form-label">Отдел</label>
                      <select class="form-select" id="department" v-model="contentForm.department_id" required>
                        <option v-for="department in departments" :key="department.id" :value="department.id">
                          {{ department.department_name }}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="access_level" class="form-label">Уровень доступа</label>
                      <select class="form-select" id="access_level" v-model="contentForm.access_level" required>
                        <option v-for="access in accessLevels" :key="access.id" :value="access.id">
                          {{ access.access_name }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="tag" class="form-label">Тег</label>
                      <select class="form-select" id="tag" v-model="contentForm.tag_id">
                        <option value="">Без категории</option>
                        <option v-for="tag in tags" :key="tag.id" :value="tag.id">
                          {{ tag.tag_name }}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="directory_path" class="form-label">Директория</label>
                      <input type="text" class="form-control" id="directory_path" v-model="contentForm.directory_path" placeholder="Укажите директорию">
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="file" class="form-label">Файл</label>
                      <input type="file" class="form-control" id="file" @change="handleFileUpload" required>
                    </div>
                  </div>
                  <button type="submit" class="btn btn-info">Загрузить</button>
                  <div v-if="uploadMessage" :class="['alert', uploadStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
                    {{ uploadMessage }}
                  </div>
                </form>
              </div>
              <!-- Вкладка инициализации LLM -->
              <div class="tab-pane fade" id="initialize" role="tabpanel" aria-labelledby="initialize-tab">
                <InitializationTable />
              </div>
              <!-- Вкладка редактирования контента -->
              <div class="tab-pane fade" id="edit" role="tabpanel" aria-labelledby="edit-tab">
                <ContentEditor :contentList="contentList" @content-updated="fetchAllContent" />
              </div>
              
              <!-- Вкладка обратной связи -->
              <div class="tab-pane fade" id="feedback" role="tabpanel" aria-labelledby="feedback-tab">
                <FeedbackAdmin />
              </div>
              
              <!-- Вкладка тестов и анкет -->
              <div class="tab-pane fade" id="quiz" role="tabpanel" aria-labelledby="quiz-tab">
                <ul class="nav nav-pills mb-3" id="quizTabs" role="tablist">
                  <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="create-quiz-tab" data-bs-toggle="pill" data-bs-target="#create-quiz" type="button" role="tab" aria-controls="create-quiz" aria-selected="true">Создание теста/анкеты</button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button class="nav-link" id="view-quizzes-tab" data-bs-toggle="pill" data-bs-target="#view-quizzes" type="button" role="tab" aria-controls="view-quizzes" aria-selected="false">Просмотр тестов/анкет</button>
                  </li>
                  <li class="nav-item" role="presentation">
                    <button class="nav-link" id="quiz-results-tab" data-bs-toggle="pill" data-bs-target="#quiz-results" type="button" role="tab" aria-controls="quiz-results" aria-selected="false">Результаты</button>
                  </li>
                </ul>
                
                <div class="tab-content" id="quizTabsContent">
                  <!-- Создание теста/анкеты -->
                  <div class="tab-pane fade show active" id="create-quiz" role="tabpanel" aria-labelledby="create-quiz-tab">
                    <form @submit.prevent="createQuiz">
                      <div class="row mb-3">
                        <div class="col-md-6">
                          <label for="quiz-title" class="form-label">Название</label>
                          <input type="text" class="form-control" id="quiz-title" v-model="quizForm.title" required>
                        </div>
                        <div class="col-md-6">
                          <label for="quiz-description" class="form-label">Описание</label>
                          <textarea class="form-control" id="quiz-description" rows="2" v-model="quizForm.description"></textarea>
                        </div>
                      </div>
                      
                      <div class="row mb-3">
                        <div class="col-md-4">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="is-test" v-model="quizForm.is_test">
                            <label class="form-check-label" for="is-test">
                              Тест (с правильными ответами)
                            </label>
                          </div>
                        </div>
                        <div class="col-md-4">
                          <label for="quiz-department" class="form-label">Отдел</label>
                          <select class="form-select" id="quiz-department" v-model="quizForm.department_id">
                            <option value="">Все отделы</option>
                            <option v-for="department in departments" :key="department.id" :value="department.id">
                              {{ department.department_name }}
                            </option>
                          </select>
                        </div>
                        <div class="col-md-4">
                          <label for="quiz-access" class="form-label">Уровень доступа</label>
                          <select class="form-select" id="quiz-access" v-model="quizForm.access_level">
                            <option value="">Все уровни доступа</option>
                            <option v-for="access in accessLevels" :key="access.id" :value="access.id">
                              {{ access.access_name }}
                            </option>
                          </select>
                        </div>
                      </div>
                      
                      <h6 class="mb-3">Вопросы</h6>
                      <div v-for="(question, index) in quizForm.questions" :key="index" class="card mb-3">
                        <div class="card-body">
                          <div class="row mb-3">
                            <div class="col-md-8">
                              <label :for="'question-text-' + index" class="form-label">Текст вопроса</label>
                              <input type="text" class="form-control" :id="'question-text-' + index" v-model="question.text" required>
                            </div>
                            <div class="col-md-3">
                              <label :for="'question-type-' + index" class="form-label">Тип вопроса</label>
                              <select class="form-select" :id="'question-type-' + index" v-model="question.question_type" required @change="handleQuestionTypeChange(question)">
                                <option value="single_choice">Одиночный выбор</option>
                                <option value="multiple_choice">Множественный выбор</option>
                                <option value="text">Текстовый ответ</option>
                              </select>
                            </div>
                            <div class="col-md-1 d-flex align-items-end">
                              <button type="button" class="btn btn-danger btn-sm" @click="removeQuestion(index)">
                                <i class="fas fa-trash"></i>
                              </button>
                            </div>
                          </div>
                          
                          <!-- Варианты ответов для вопросов с выбором -->
                          <div v-if="question.question_type === 'single_choice' || question.question_type === 'multiple_choice'">
                            <div class="row mb-2">
                              <div class="col-12">
                                <label class="form-label">Варианты ответов</label>
                              </div>
                            </div>
                            <div v-for="(option, optIndex) in question.options || []" :key="optIndex" class="row mb-2">
                              <div class="col-md-6">
                                <div class="input-group">
                                  <input type="text" class="form-control" v-model="option.text" placeholder="Вариант ответа" required>
                                  <button type="button" class="btn btn-outline-danger" @click="removeOption(question, optIndex)">
                                    <i class="fas fa-times"></i>
                                  </button>
                                </div>
                              </div>
                              <div class="col-md-6" v-if="quizForm.is_test">
                                <div class="form-check" v-if="question.question_type === 'single_choice'">
                                  <input class="form-check-input" type="radio" :name="'correct-' + index" :id="'correct-' + index + '-' + optIndex" :value="String(option.id)" v-model="question.correct_answer">
                                  <label class="form-check-label" :for="'correct-' + index + '-' + optIndex">
                                    Правильный ответ
                                  </label>
                                </div>
                                <div class="form-check" v-else>
                                  <input class="form-check-input" type="checkbox" :id="'correct-' + index + '-' + optIndex" :value="String(option.id)" v-model="question.correct_answer">
                                  <label class="form-check-label" :for="'correct-' + index + '-' + optIndex">
                                    Правильный ответ
                                  </label>
                                </div>
                              </div>
                            </div>
                            <button type="button" class="btn btn-sm btn-outline-primary mt-2" @click="addOption(question)">
                              <i class="fas fa-plus"></i> Добавить вариант
                            </button>
                          </div>
                          
                          <!-- Правильный ответ для текстовых вопросов -->
                          <div v-else-if="question.question_type === 'text' && quizForm.is_test" class="row mt-3">
                            <div class="col-md-6">
                              <label :for="'correct-answer-' + index" class="form-label">Правильный ответ</label>
                              <input type="text" class="form-control" :id="'correct-answer-' + index" v-model="question.correct_answer" required>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div class="mb-3">
                        <button type="button" class="btn btn-info" @click="addQuestion">
                          <i class="fas fa-plus"></i> Добавить вопрос
                        </button>
                      </div>
                      
                      <button type="submit" class="btn btn-info" :disabled="quizForm.questions.length === 0">Создать тест/анкету</button>
                      <div v-if="quizMessage" :class="['alert', quizStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
                        {{ quizMessage }}
                      </div>
                    </form>
                  </div>
                  
                  <!-- Просмотр тестов/анкет -->
                  <div class="tab-pane fade" id="view-quizzes" role="tabpanel" aria-labelledby="view-quizzes-tab">
                    <div class="row mb-3">
                      <div class="col-md-4">
                        <select class="form-select" v-model="quizFilter.type">
                          <option value="all">Все</option>
                          <option value="test">Только тесты</option>
                          <option value="survey">Только анкеты</option>
                        </select>
                      </div>
                      <div class="col-md-4">
                        <select class="form-select" v-model="quizFilter.department">
                          <option value="all">Все отделы</option>
                          <option v-for="department in departments" :key="department.id" :value="department.id">
                            {{ department.department_name }}
                          </option>
                        </select>
                      </div>
                      <div class="col-md-4">
                        <button class="btn btn-primary w-100" @click="fetchQuizzes">
                          <i class="fas fa-search"></i> Применить фильтры
                        </button>
                      </div>
                    </div>
                    
                    <div v-if="loadingQuizzes" class="text-center py-4">
                      <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Загрузка...</span>
                      </div>
                      <p class="mt-2">Загрузка тестов и анкет...</p>
                    </div>
                    
                    <div v-else-if="quizzesError" class="alert alert-danger">
                      {{ quizzesError }}
                    </div>
                    
                    <div v-else-if="quizzes.length === 0" class="alert alert-info">
                      Тесты и анкеты не найдены
                    </div>
                    
                    <div v-else class="table-responsive">
                      <table class="table table-hover">
                        <thead>
                          <tr>
                            <th>Название</th>
                            <th>Тип</th>
                            <th>Описание</th>
                            <th>Отдел</th>
                            <th>Уровень доступа</th>
                            <th>Вопросов</th>
                            <th>Дата создания</th>
                            <th>Действия</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="quiz in quizzes" :key="quiz.id">
                            <td>{{ quiz.title }}</td>
                            <td>
                              <span :class="['badge', quiz.is_test ? 'bg-primary' : 'bg-info']">
                                {{ quiz.is_test ? 'Тест' : 'Анкета' }}
                              </span>
                            </td>
                            <td>{{ quiz.description || 'Нет описания' }}</td>
                            <td>{{ getDepartmentName(quiz.department_id) || 'Все отделы' }}</td>
                            <td>{{ getAccessLevelName(quiz.access_level) || 'Все уровни' }}</td>
                            <td>{{ quiz.question_count }}</td>
                            <td>{{ formatDate(quiz.created_at) }}</td>
                            <td>
                              <button class="btn btn-sm btn-primary me-2" @click="viewQuizDetails(quiz.id)">
                                <i class="fas fa-eye"></i>
                              </button>
                              <button class="btn btn-sm btn-danger" @click="deleteQuiz(quiz.id)">
                                <i class="fas fa-trash"></i>
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    
                    <!-- Модальное окно для просмотра деталей теста/анкеты -->
                    <div class="modal fade" id="quizDetailsModal" tabindex="-1" aria-labelledby="quizDetailsModalLabel" aria-hidden="true">
                      <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="quizDetailsModalLabel">{{ selectedQuiz ? selectedQuiz.title : '' }}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                            <div v-if="loadingQuizDetails" class="text-center py-4">
                              <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Загрузка...</span>
                              </div>
                              <p class="mt-2">Загрузка деталей...</p>
                            </div>
                            
                            <div v-else-if="quizDetailsError" class="alert alert-danger">
                              {{ quizDetailsError }}
                            </div>
                            
                            <div v-else-if="selectedQuiz">
                              <div class="mb-4">
                                <p><strong>Описание:</strong> {{ selectedQuiz.description || 'Нет описания' }}</p>
                                <p>
                                  <strong>Тип:</strong> 
                                  <span :class="['badge', selectedQuiz.is_test ? 'bg-primary' : 'bg-info']">
                                    {{ selectedQuiz.is_test ? 'Тест' : 'Анкета' }}
                                  </span>
                                </p>
                                <p><strong>Отдел:</strong> {{ getDepartmentName(selectedQuiz.department_id) || 'Все отделы' }}</p>
                                <p><strong>Уровень доступа:</strong> {{ getAccessLevelName(selectedQuiz.access_level) || 'Все уровни' }}</p>
                                <p><strong>Дата создания:</strong> {{ formatDate(selectedQuiz.created_at) }}</p>
                              </div>
                              
                              <h6 class="mb-3">Вопросы:</h6>
                              <div v-for="(question, index) in selectedQuiz.questions" :key="question.id" class="card mb-3">
                                <div class="card-body">
                                  <h6>{{ index + 1 }}. {{ question.text }}</h6>
                                  <p class="text-muted">
                                    Тип: {{ questionTypeLabels[question.question_type] || question.question_type }}
                                  </p>
                                  
                                  <div v-if="question.question_type === 'single_choice' || question.question_type === 'multiple_choice'">
                                    <p><strong>Варианты ответов:</strong></p>
                                    <ul class="list-group">
                                      <li v-for="option in question.options || []" :key="option.id" class="list-group-item" :class="{ 'list-group-item-success': isCorrectOption(question, option.id) }">
                                        {{ option.text }}
                                        <span v-if="isCorrectOption(question, option.id)" class="badge bg-success ms-2">Правильный</span>
                                      </li>
                                    </ul>
                                  </div>
                                  
                                  <div v-else-if="question.question_type === 'text' && selectedQuiz.is_test" class="mt-3">
                                    <p><strong>Правильный ответ:</strong> {{ question.correct_answer }}</p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- Результаты тестов/анкет -->
                  <div class="tab-pane fade" id="quiz-results" role="tabpanel" aria-labelledby="quiz-results-tab">
                    <div class="row mb-3">
                      <div class="col-md-6">
                        <label for="results-quiz-select" class="form-label">Выберите тест/анкету</label>
                        <select class="form-select" id="results-quiz-select" v-model="resultsQuizId" @change="fetchQuizStatistics">
                          <option value="">Выберите тест/анкету</option>
                          <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
                            {{ quiz.title }} ({{ quiz.is_test ? 'Тест' : 'Анкета' }})
                          </option>
                        </select>
                      </div>
                      <div class="col-md-6">
                        <label for="results-user-select" class="form-label">Пользователь</label>
                        <select class="form-select" id="results-user-select" v-model="resultsUserId" @change="fetchUserAttempts">
                          <option value="">Все пользователи</option>
                          <option v-for="user in users" :key="user.id" :value="user.id">
                            {{ user.login }}
                          </option>
                        </select>
                      </div>
                    </div>
                    
                    <div v-if="loadingResults" class="text-center py-4">
                      <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Загрузка...</span>
                      </div>
                      <p class="mt-2">Загрузка результатов...</p>
                    </div>
                    
                    <div v-else-if="resultsError" class="alert alert-danger">
                      {{ resultsError }}
                    </div>
                    
                    <div v-else-if="!resultsQuizId" class="alert alert-info">
                      Выберите тест или анкету для просмотра результатов
                    </div>
                    
                    <div v-else>
                      <!-- Общая статистика по тесту/анкете -->
                      <div v-if="quizStatistics" class="card mb-4">
                        <div class="card-header">
                          <h6>Общая статистика</h6>
                        </div>
                        <div class="card-body">
                          <div class="row">
                            <div class="col-md-3">
                              <div class="card bg-gradient-primary">
                                <div class="card-body p-3">
                                  <h6 class="text-white mb-0">Всего попыток</h6>
                                  <h4 class="text-white">{{ quizStatistics.attempts_count }}</h4>
                                </div>
                              </div>
                            </div>
                            <div class="col-md-3">
                              <div class="card bg-gradient-info">
                                <div class="card-body p-3">
                                  <h6 class="text-white mb-0">Уникальных пользователей</h6>
                                  <h4 class="text-white">{{ quizStatistics.unique_users_count }}</h4>
                                </div>
                              </div>
                            </div>
                            <div class="col-md-3" v-if="quizStatistics.is_test">
                              <div class="card bg-gradient-success">
                                <div class="card-body p-3">
                                  <h6 class="text-white mb-0">Средний балл</h6>
                                  <h4 class="text-white">{{ quizStatistics.avg_score ? quizStatistics.avg_score.toFixed(1) : '0' }}</h4>
                                </div>
                              </div>
                            </div>
                          </div>
                          
                          <!-- Статистика по вопросам для тестов -->
                          <div v-if="quizStatistics.is_test && quizStatistics.question_stats" class="mt-4">
                            <h6>Статистика по вопросам</h6>
                            <div class="table-responsive">
                              <table class="table table-sm">
                                <thead>
                                  <tr>
                                    <th>Вопрос</th>
                                    <th>Правильных ответов</th>
                                    <th>Всего ответов</th>
                                    <th>% правильных</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="stat in quizStatistics.question_stats" :key="stat.question_id">
                                    <td>{{ stat.text }}</td>
                                    <td>{{ stat.correct_answers }}</td>
                                    <td>{{ stat.total_answers }}</td>
                                    <td>
                                      <div class="progress" style="height: 6px;">
                                        <div class="progress-bar bg-gradient-success" :style="{ width: stat.correct_percentage + '%' }"></div>
                                      </div>
                                      <span class="ms-1">{{ stat.correct_percentage.toFixed(1) }}%</span>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Попытки пользователей -->
                      <div v-if="userAttempts.length > 0" class="card">
                        <div class="card-header">
                          <h6>{{ resultsUserId ? 'Попытки пользователя' : 'Последние попытки' }}</h6>
                        </div>
                        <div class="card-body">
                          <div class="table-responsive">
                            <table class="table table-hover">
                              <thead>
                                <tr>
                                  <th>Пользователь</th>
                                  <th>Дата</th>
                                  <th v-if="quizStatistics.is_test">Результат</th>
                                  <th>Действия</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="attempt in userAttempts" :key="attempt.id">
                                  <td>{{ getUserName(attempt.user_id) }}</td>
                                  <td>{{ formatDate(attempt.completed_at || attempt.started_at) }}</td>
                                  <td v-if="quizStatistics.is_test">
                                    {{ attempt.score !== null ? attempt.score + ' / ' + attempt.total_questions : '-' }}
                                    <div v-if="attempt.score !== null" class="progress" style="height: 6px;">
                                      <div class="progress-bar bg-gradient-success" :style="{ width: (attempt.score / attempt.total_questions * 100) + '%' }"></div>
                                    </div>
                                  </td>
                                  <td>
                                    <button class="btn btn-sm btn-info" @click="viewAttemptDetails(attempt.id)">
                                      <i class="fas fa-eye"></i> Детали
                                    </button>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                      
                      <div v-else-if="!loadingResults && resultsQuizId" class="alert alert-info">
                        Нет данных о попытках для выбранного теста/анкеты
                      </div>
                    </div>
                    
                    <!-- Модальное окно для просмотра деталей попытки -->
                    <div class="modal fade" id="attemptDetailsModal" tabindex="-1" aria-labelledby="attemptDetailsModalLabel" aria-hidden="true">
                      <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="attemptDetailsModalLabel">Детали попытки</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                            <div v-if="loadingAttemptDetails" class="text-center py-4">
                              <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Загрузка...</span>
                              </div>
                              <p class="mt-2">Загрузка деталей...</p>
                            </div>
                            
                            <div v-else-if="attemptDetailsError" class="alert alert-danger">
                              {{ attemptDetailsError }}
                            </div>
                            
                            <div v-else-if="selectedAttempt">
                              <div class="mb-3">
                                <p><strong>Пользователь:</strong> {{ getUserName(selectedAttempt.user_id) }}</p>
                                <p><strong>Дата:</strong> {{ formatDate(selectedAttempt.completed_at || selectedAttempt.started_at) }}</p>
                                <p v-if="selectedAttempt.score !== null"><strong>Результат:</strong> {{ selectedAttempt.score }} баллов</p>
                              </div>
                              
                              <h6>Ответы:</h6>
                              <div class="list-group">
                                <div v-for="answer in selectedAttempt.answers" :key="answer.id" class="list-group-item" :class="{ 'list-group-item-success': answer.is_correct === true, 'list-group-item-danger': answer.is_correct === false }">
                                  <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1">{{ getQuestionText(answer.question_id) }}</h6>
                                    <small v-if="answer.is_correct !== null" :class="answer.is_correct ? 'text-success' : 'text-danger'">
                                      {{ answer.is_correct ? 'Верно' : 'Неверно' }}
                                    </small>
                                  </div>
                                  <p class="mb-1"><strong>Ответ:</strong> {{ formatAnswerText(answer) }}</p>
                                  <small v-if="answer.is_correct === false" class="text-muted">
                                    <strong>Правильный ответ:</strong> {{ getCorrectAnswerText(answer.question_id) }}
                                  </small>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
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
import AuthorsTable from "./components/AuthorsTable.vue";
import ContentTable from "./components/ContentTable.vue";
import InitializationTable from "./components/InitializationTable.vue";
import ContentEditor from "./components/ContentEditor.vue";
import FeedbackAdmin from "./components/FeedbackAdmin.vue";
import axios from 'axios';
import * as bootstrap from 'bootstrap';

export default {
  name: "TablesPage",
  components: {
    AuthorsTable,
    ContentTable,
    InitializationTable,
    ContentEditor,
    FeedbackAdmin
  },
  data() {
    return {
      // Форма регистрации пользователя
      registerForm: {
        login: '',
        password: '',
        role_id: 2,
        department_id: null,
        access_id: null
      },
      registerMessage: '',
      registerStatus: false,
      
      // Форма загрузки контента
      contentForm: {
        title: '',
        description: '',
        department_id: null,
        access_level: null,
        tag_id: null,
        file: null,
        directory_path: ''
      },
      uploadMessage: '',
      uploadStatus: false,
      
      // Списки для выпадающих меню
      departments: [],
      accessLevels: [],
      llmModels: [],
      embeddingModels: [],
      tags: [],
      
      // Список всего контента
      contentList: [],
      
      // Форма для создания теста/анкеты
      quizForm: {
        title: '',
        description: '',
        is_test: false,
        department_id: null,
        access_level: null,
        questions: []
      },
      quizMessage: '',
      quizStatus: false,
      
      // Фильтры для просмотра тестов/анкет
      quizFilter: {
        type: 'all',
        department: 'all'
      },
      loadingQuizzes: false,
      quizzes: [],
      quizzesError: '',
      
      // Форма для просмотра деталей теста/анкеты
      selectedQuiz: null,
      loadingQuizDetails: false,
      quizDetailsError: '',
      
      // Результаты теста/анкеты
      resultsQuizId: '',
      loadingResults: false,
      resultsError: '',
      quizStatistics: null,
      userAttempts: [],
      
      // Дополнительные данные для тестов/анкет
      questionTypeLabels: {
        single_choice: 'Одиночный выбор',
        multiple_choice: 'Множественный выбор',
        text: 'Текстовый ответ'
      },
      selectedAttempt: null,
      loadingAttemptDetails: false,
      attemptDetailsError: '',
      resultsUserId: '',
      
      // Модальные окна
      quizDetailsModal: null,
      attemptDetailsModal: null,
      
      // Список пользователей
      users: []
    };
  },
  async created() {
    await this.fetchDepartments();
    await this.fetchAccessLevels();
    await this.fetchLLMModels();
    await this.fetchEmbeddingModels();
    await this.fetchTags();
    await this.fetchAllContent();
    await this.fetchUsers();
    await this.fetchQuizzes();
  },
  mounted() {
    // Инициализация модальных окон
    this.quizDetailsModal = new bootstrap.Modal(document.getElementById('quizDetailsModal'));
    this.attemptDetailsModal = new bootstrap.Modal(document.getElementById('attemptDetailsModal'));
  },
  methods: {
    // Получение списка отделов
    async fetchDepartments() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/departments`);
        this.departments = response.data;
      } catch (error) {
        console.error('Ошибка при получении отделов:', error);
        this.departments = [];
      }
    },
    
    // Получение списка уровней доступа
    async fetchAccessLevels() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/access_levels`);
        this.accessLevels = response.data;
      } catch (error) {
        console.error('Ошибка при получении отделов:', error);
        this.accessLevels = [];
      }
    },
    
    // Получение списка моделей LLM
    async fetchLLMModels() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/llm/models/llm`);
        if (response.data && response.data.models) {
          this.llmModels = response.data.models;
        } else {
          // Fallback на дефолтные значения, если API не вернул моделей
          this.llmModels = [
            'mistral',
            'llama3',
            'ilyagusev/saiga_llama3:latest',
            'gemma'
          ];
        }
      } catch (error) {
        console.error('Ошибка при получении моделей LLM:', error);
        // Fallback на дефолтные значения в случае ошибки
        this.llmModels = [
          'snowflake-arctic-embed2:latest ',
          'llama3',
          'ilyagusev/saiga_llama3',
          'gemma'
        ];
      }
    },
    
    // Получение списка моделей эмбеддингов
    async fetchEmbeddingModels() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/llm/models/embedding`);
        if (response.data && response.data.models) {
          this.embeddingModels = response.data.models;
        } else {
          // Fallback на дефолтные значения, если API не вернул моделей
          this.embeddingModels = [
            'snowflake-arctic-embed2:latest ',
            'mxbai-embed-large',
            'all-minilm'
          ];
        }
      } catch (error) {
        console.error('Ошибка при получении моделей эмбеддингов:', error);
        // Fallback на дефолтные значения в случае ошибки
        this.embeddingModels = [
          'snowflake-arctic-embed2:latest',
          'mxbai-embed-large',
          'all-minilm'
        ];
      }
    },
    
    // Получение списка тегов
    async fetchTags() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/tags`);
        this.tags = response.data.tags;
      } catch (error) {
        console.error('Ошибка при получении тегов:', error);
      }
    },
    
    // Получение списка всего контента
    async fetchAllContent() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/content/all`);
        this.contentList = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка контента:', error);
        this.contentList = [];
      }
    },
    
    // Регистрация пользователя
    async registerUser() {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/user/register`, this.registerForm);
        this.registerMessage = 'Пользователь успешно зарегистрирован!';
        this.registerStatus = true;
        
        // Очистка формы
        this.registerForm = {
          login: '',
          password: '',
          role_id: 2,
          department_id: null,
          access_id: null
        };
        
        // Обновляем список пользователей
        const authorsTableRef = this.$refs.authorsTable;
        if (authorsTableRef && typeof authorsTableRef.fetchUsers === 'function') {
          authorsTableRef.fetchUsers();
        }
      } catch (error) {
        this.registerMessage = error.response?.data?.detail || 'Ошибка при регистрации пользователя';
        this.registerStatus = false;
        console.error('Ошибка регистрации:', error);
      }
    },
    
    // Обработка загрузки файла
    handleFileUpload(event) {
      this.contentForm.file = event.target.files[0];
    },
    
    // Загрузка контента
    async uploadContent() {
      try {
        if (!this.contentForm.title || !this.contentForm.description || !this.contentForm.department_id || 
            !this.contentForm.access_level || !this.contentForm.file || !this.contentForm.directory_path) {
          this.uploadMessage = 'Все поля должны быть заполнены';
          this.uploadStatus = false;
          return;
        }

        const formData = new FormData();
        formData.append('file', this.contentForm.file);
        
        // Отправляем запрос с параметрами в URL-строке
        const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/content/upload-content?title=${encodeURIComponent(this.contentForm.title)}` +
            `&description=${encodeURIComponent(this.contentForm.description)}` +
            `&access_id=${this.contentForm.access_level}` +
            `&department_id=${this.contentForm.department_id}` +
            `&tag_id=${this.contentForm.tag_id || ''}` +
            `&directory_path=${encodeURIComponent(this.contentForm.directory_path)}`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        );
        
        this.uploadMessage = 'Контент успешно загружен!';
        this.uploadStatus = true;
        
        // Очистка формы
        this.contentForm = {
          title: '',
          description: '',
          department_id: null,
          access_level: null,
          tag_id: null,
          file: null,
          directory_path: ''
        };
        
        // Сбрасываем поле загрузки файла
        document.getElementById('file').value = '';
        
        // Обновляем таблицу контента
        const contentTableRef = this.$refs.contentTable;
        if (contentTableRef && typeof contentTableRef.fetchAllContent === 'function') {
          contentTableRef.fetchAllContent();
        }
        
      } catch (error) {
        this.uploadMessage = error.response?.data?.detail || 'Ошибка при загрузке контента';
        this.uploadStatus = false;
        console.error('Ошибка загрузки контента:', error);
      }
    },
    
    // Создание нового теста/анкеты
    async createQuiz() {
      try {
        const quizData = JSON.parse(JSON.stringify(this.quizForm));
        
        quizData.questions.forEach(question => {
          if (question.question_type === 'single_choice' && question.correct_answer) {
            question.correct_answer = parseInt(question.correct_answer);
          }
          
          if (question.question_type === 'multiple_choice' && Array.isArray(question.correct_answer)) {
            question.correct_answer = question.correct_answer.map(id => parseInt(id));
          }
          
          if (!question.options) {
            question.options = [];
          }
        });
        
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/quiz/create`, quizData);
        this.quizMessage = 'Тест/анкета успешно создана!';
        this.quizStatus = true;
        
        this.quizForm = {
          title: '',
          description: '',
          is_test: false,
          department_id: null,
          access_level: null,
          questions: []
        };
        
        await this.fetchQuizzes();
      } catch (error) {
        console.error('Ошибка создания теста/анкеты:', error);
        this.quizMessage = error.response?.data?.detail || 'Ошибка при создании теста/анкеты';
        this.quizStatus = false;
      }
    },
    
    // Получение списка тестов/анкет
    async fetchQuizzes() {
      this.loadingQuizzes = true;
      this.quizzesError = '';
      this.quizzes = [];
      
      try {
        let params = {};
        if (this.quizFilter.type !== 'all') {
          params.is_test = this.quizFilter.type === 'test';
        }
        if (this.quizFilter.department !== 'all') {
          params.department_id = this.quizFilter.department;
        }
        
        // Используем новый эндпоинт для администраторов
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/admin/list`, { params });
        this.quizzes = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка тестов/анкет:', error);
        this.quizzesError = error.response?.data?.detail || 'Ошибка при получении списка тестов/анкет';
      } finally {
        this.loadingQuizzes = false;
      }
    },
    
    // Получение деталей теста/анкеты
    async viewQuizDetails(id) {
      this.loadingQuizDetails = true;
      this.quizDetailsError = '';
      this.selectedQuiz = null;
      
      try {
        const currentUser = JSON.parse(localStorage.getItem('user')) || {};
        const userId = currentUser.id || 1;
        
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/${id}?user_id=${userId}`);
        this.selectedQuiz = response.data;
        this.quizDetailsModal.show();
      } catch (error) {
        this.quizDetailsError = error.response?.data?.detail || 'Ошибка при получении деталей теста/анкеты';
      } finally {
        this.loadingQuizDetails = false;
      }
    },
    
    // Удаление теста/анкеты
    async deleteQuiz(id) {
      if (confirm('Вы уверены, что хотите удалить этот тест/анкету?')) {
        try {
          const response = await axios.delete(`${import.meta.env.VITE_API_URL}/quiz/${id}`);
          this.quizMessage = 'Тест/анкета успешно удалена!';
          this.quizStatus = true;
          
          await this.fetchQuizzes();
        } catch (error) {
          this.quizMessage = error.response?.data?.detail || 'Ошибка при удалении теста/анкеты';
          this.quizStatus = false;
          console.error('Ошибка удаления теста/анкеты:', error);
        }
      }
    },
    
    // Получение статистики теста/анкеты
    async fetchQuizStatistics() {
      this.loadingResults = true;
      this.resultsError = '';
      this.quizStatistics = null;
      this.userAttempts = [];
      
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/stats/${this.resultsQuizId}`);
        this.quizStatistics = response.data;
        
        if (this.resultsUserId) {
          await this.fetchUserAttempts();
        } else {
          const userAttemptsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/attempts?quiz_id=${this.resultsQuizId}`);
          this.userAttempts = userAttemptsResponse.data;
        }
      } catch (error) {
        this.resultsError = error.response?.data?.detail || 'Ошибка при получении статистики теста/анкеты';
      } finally {
        this.loadingResults = false;
      }
    },
    
    // Получение попыток пользователя
    async fetchUserAttempts() {
      this.loadingResults = true;
      this.resultsError = '';
      this.userAttempts = [];
      
      try {
        let url = `${import.meta.env.VITE_API_URL}/quiz/attempts/${this.resultsUserId}`;
        if (this.resultsQuizId) {
          url += `?quiz_id=${this.resultsQuizId}`;
        }
        const response = await axios.get(url);
        this.userAttempts = response.data;
      } catch (error) {
        this.resultsError = error.response?.data?.detail || 'Ошибка при получении попыток пользователя';
      } finally {
        this.loadingResults = false;
      }
    },
    
    // Получение деталей попытки
    async viewAttemptDetails(id) {
      this.loadingAttemptDetails = true;
      this.attemptDetailsError = '';
      this.selectedAttempt = null;
      
      try {
        const currentUser = JSON.parse(localStorage.getItem('user')) || {};
        const userId = currentUser.id || 1;
        
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/quiz/attempt/${id}?user_id=${userId}`);
        this.selectedAttempt = response.data;
        this.attemptDetailsModal.show();
      } catch (error) {
        this.attemptDetailsError = error.response?.data?.detail || 'Ошибка при получении деталей попытки';
      } finally {
        this.loadingAttemptDetails = false;
      }
    },
    
    // Методы для работы с вопросами и вариантами ответов
    addQuestion() {
      const newQuestionId = Date.now();
      this.quizForm.questions.push({
        text: '',
        question_type: 'single_choice',
        options: [
          { id: newQuestionId + 1, text: '' },
          { id: newQuestionId + 2, text: '' }
        ],
        correct_answer: '',
        order: this.quizForm.questions.length + 1
      });
    },
    
    removeQuestion(index) {
      this.quizForm.questions.splice(index, 1);
    },
    
    addOption(question) {
      const newId = question.options.length > 0 
        ? Math.max(...question.options.map(o => o.id)) + 1 
        : Date.now();
      
      question.options.push({
        id: newId,
        text: ''
      });
      
      if (question.question_type === 'multiple_choice' && !Array.isArray(question.correct_answer)) {
        question.correct_answer = [];
      }
    },
    
    removeOption(question, index) {
      const optionId = question.options[index].id;
      
      if (question.question_type === 'single_choice' && question.correct_answer === optionId) {
        question.correct_answer = '';
      } else if (question.question_type === 'multiple_choice' && Array.isArray(question.correct_answer)) {
        question.correct_answer = question.correct_answer.filter(id => id !== optionId);
      }
      
      question.options.splice(index, 1);
    },
    
    handleQuestionTypeChange(question) {
      if (question.question_type === 'single_choice') {
        question.correct_answer = question.options && question.options.length > 0 ? 
          String(question.options[0].id) : '';
      } else if (question.question_type === 'multiple_choice') {
        question.correct_answer = [];
      } else if (question.question_type === 'text') {
        question.correct_answer = '';
      }
      
      if (question.options === undefined || question.options === null) {
        const newOptionId = Date.now();
        question.options = [
          { id: newOptionId + 1, text: '' },
          { id: newOptionId + 2, text: '' }
        ];
      }
    },
    
    getDepartmentName(id) {
      if (!id) return null;
      const department = this.departments.find(d => d.id === id);
      return department ? department.department_name : id;
    },
    
    getAccessLevelName(id) {
      if (!id) return null;
      const access = this.accessLevels.find(a => a.id === id);
      return access ? access.access_name : id;
    },
    
    getUserName(id) {
      const user = this.users?.find(u => u.id === id);
      return user ? user.login : `Пользователь #${id}`;
    },
    
    isCorrectOption(question, optionId) {
      if (!question.correct_answer) return false;
      
      if (question.question_type === 'single_choice') {
        const correctAnswer = typeof question.correct_answer === 'number' ? 
          question.correct_answer : parseInt(question.correct_answer);
        return correctAnswer === optionId;
      } else if (question.question_type === 'multiple_choice' && Array.isArray(question.correct_answer)) {
        return question.correct_answer.some(id => {
          const correctId = typeof id === 'string' ? parseInt(id) : id;
          return correctId === optionId;
        });
      }
      
      return false;
    },
    
    getQuestionText(questionId) {
      if (!this.selectedQuiz || !this.selectedQuiz.questions) return '';
      
      const question = this.selectedQuiz.questions.find(q => q.id === questionId);
      return question ? question.text : '';
    },
    
    getCorrectAnswerText(questionId) {
      if (!this.selectedQuiz || !this.selectedQuiz.questions) return '';
      
      const question = this.selectedQuiz.questions.find(q => q.id === questionId);
      if (!question || !question.correct_answer) return '';
      
      if (question.question_type === 'single_choice') {
        const correctId = typeof question.correct_answer === 'string' ? 
          parseInt(question.correct_answer) : question.correct_answer;
        const option = (question.options || []).find(o => o.id === correctId);
        return option ? option.text : '';
      } else if (question.question_type === 'multiple_choice' && Array.isArray(question.correct_answer)) {
        const correctIds = question.correct_answer.map(id => 
          typeof id === 'string' ? parseInt(id) : id);
        const selectedOptions = (question.options || []).filter(o => 
          correctIds.includes(o.id));
        return selectedOptions.map(o => o.text).join(', ');
      }
      
      return question.correct_answer;
    },
    
    formatAnswerText(answer) {
      if (!answer || !answer.answer) return '-';
      
      if (!this.selectedQuiz || !this.selectedQuiz.questions) return String(answer.answer);
      
      const question = this.selectedQuiz.questions.find(q => q.id === answer.question_id);
      if (!question) return JSON.stringify(answer.answer);
      
      if (question.question_type === 'single_choice') {
        const answerId = typeof answer.answer === 'string' ? 
          parseInt(answer.answer) : answer.answer;
        const option = (question.options || []).find(o => o.id === answerId);
        return option ? option.text : answer.answer;
      } else if (question.question_type === 'multiple_choice' && Array.isArray(answer.answer)) {
        // Преобразуем IDs в числа для корректного сравнения
        const answerIds = answer.answer.map(id => 
          typeof id === 'string' ? parseInt(id) : id);
        const selectedOptions = (question.options || []).filter(o => 
          answerIds.includes(o.id));
        return selectedOptions.map(o => o.text).join(', ');
      }
      
      return answer.answer;
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    // Получение списка пользователей
    async fetchUsers() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/users`);
        this.users = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка пользователей:', error);
        this.users = [];
      }
    },
  }
};
</script>

<style scoped>
.nav-tabs .nav-link {
  color: #344767;
}

.nav-tabs .nav-link.active {
  color: #344767;
  font-weight: 600;
  border-bottom: 2px solid #172d76;
}

.form-label {
  color: #344767;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-control, .form-select {
  border: 1px solid #d2d6da;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 400;
  line-height: 1.4rem;
  color: #495057;
  border-radius: 0.5rem;
  transition: 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #82d616;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(130, 214, 22, 0.25);
}
.btn-info {
  background-color: #172d76;
  border-color: #7b7b7b;
  &:hover {
    background-color: #344785;
    border-color: #7b7b7b;
  }
}
.bg-gradient-info {
  background-color: #173376;
  border-color: #7b7b7b;
}
</style>
