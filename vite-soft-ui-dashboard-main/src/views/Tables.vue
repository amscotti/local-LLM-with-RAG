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
                <button class="nav-link" id="initialize-tab" data-bs-toggle="tab" data-bs-target="#initialize" type="button" role="tab" aria-controls="initialize" aria-selected="false">Инициализация LLM</button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="edit-tab" data-bs-toggle="tab" data-bs-target="#edit" type="button" role="tab" aria-controls="edit" aria-selected="false">Редактирование контента</button>
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
                  <button type="submit" class="btn bg-gradient-success">Зарегистрировать</button>
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
                      <label for="file" class="form-label">Файл</label>
                      <input type="file" class="form-control" id="file" @change="handleFileUpload" required>
                    </div>
                  </div>
                  <button type="submit" class="btn bg-gradient-success">Загрузить</button>
                  <div v-if="uploadMessage" :class="['alert', uploadStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
                    {{ uploadMessage }}
                  </div>
                </form>
              </div>
              
              <!-- Вкладка инициализации LLM -->
              <div class="tab-pane fade" id="initialize" role="tabpanel" aria-labelledby="initialize-tab">
                <form @submit.prevent="initializeLLM">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="model-name" class="form-label">Модель LLM</label>
                      <input type="text" class="form-control" id="model-name" v-model="initializeForm.model_name" required placeholder="Введите модель LLM">
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="embedding-model" class="form-label">Модель эмбеддингов</label>
                      <input type="text" class="form-control" id="embedding-model" v-model="initializeForm.embedding_model_name" required placeholder="Введите модель эмбеддингов">
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-12 mb-3">
                      <label for="documents-path" class="form-label">Путь к документам</label>
                      <input type="text" class="form-control" id="documents-path" v-model="initializeForm.documents_path" placeholder="Например: Research" required>
                      <small class="text-muted">Укажите путь к директории с документами для индексации</small>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-12 mb-3">
                      <label for="department-id" class="form-label">Идентификатор отдела</label>
                      <input type="text" class="form-control" id="department-id" v-model="initializeForm.department_id" required placeholder="Введите идентификатор отдела">
                      <small class="text-muted">Укажите идентификатор отдела для создания уникальной базы данных</small>
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-12">
                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="confirm-init" v-model="initializeForm.confirm">
                        <label class="form-check-label" for="confirm-init">
                          Я подтверждаю, что хочу инициализировать LLM. Это может занять некоторое время.
                        </label>
                      </div>
                    </div>
                  </div>
                  <button type="submit" class="btn bg-gradient-success" :disabled="!initializeForm.confirm || isInitializing">
                    <span v-if="isInitializing" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ isInitializing ? 'Инициализация...' : 'Инициализировать LLM' }}
                  </button>
                  <div v-if="initializeMessage" :class="['alert', initializeStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
                    {{ initializeMessage }}
                  </div>
                </form>
              </div>
              
              <!-- Вкладка редактирования контента -->
              <div class="tab-pane fade" id="edit" role="tabpanel" aria-labelledby="edit-tab">
                <div class="row mb-4">
                  <div class="col-12">
                    <div class="form-group">
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
                      <textarea class="form-control" id="edit-description" rows="3" v-model="editForm.description"></textarea>
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
                  <button type="submit" class="btn bg-gradient-success">Сохранить изменения</button>
                  <div v-if="editMessage" :class="['alert', editStatus ? 'alert-success' : 'alert-danger', 'mt-3']">
                    {{ editMessage }}
                  </div>
                </form>
                <div v-else class="alert alert-info">
                  Выберите контент для редактирования
                </div>
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
                            <div v-for="(option, optIndex) in question.options" :key="optIndex" class="row mb-2">
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
                        <button type="button" class="btn btn-outline-primary" @click="addQuestion">
                          <i class="fas fa-plus"></i> Добавить вопрос
                        </button>
                      </div>
                      
                      <button type="submit" class="btn bg-gradient-success" :disabled="quizForm.questions.length === 0">Создать тест/анкету</button>
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
                              <button class="btn btn-sm btn-info me-2" @click="viewQuizDetails(quiz.id)">
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
                                      <li v-for="option in question.options" :key="option.id" class="list-group-item" :class="{ 'list-group-item-success': isCorrectOption(question, option.id) }">
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
import axios from 'axios';
import * as bootstrap from 'bootstrap';

export default {
  name: "TablesPage",
  components: {
    AuthorsTable,
    ContentTable,
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
        file: null
      },
      uploadMessage: '',
      uploadStatus: false,
      
      // Форма инициализации LLM
      initializeForm: {
        model_name: '',
        embedding_model_name: '',
        documents_path: 'Research',
        confirm: false,
        department_id: null
      },
      initializeMessage: '',
      initializeStatus: false,
      isInitializing: false,
      
      // Списки для выпадающих меню
      departments: [],
      accessLevels: [],
      llmModels: [],
      embeddingModels: [],
      tags: [],
      
      // Форма редактирования контента
      editForm: {
        id: '',
        title: '',
        description: '',
        department_id: null,
        access_level: null,
        tag_id: null
      },
      editMessage: '',
      editStatus: false,
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
        const response = await axios.get(`http://192.168.81.149:8000/api/departments`);
        this.departments = response.data;
      } catch (error) {
        console.error('Ошибка при получении отделов:', error);
        this.departments = [];
      }
    },
    
    // Получение списка уровней доступа
    async fetchAccessLevels() {
      try {
        const response = await axios.get(`http://192.168.81.149:8000/api/access_levels`);
        this.accessLevels = response.data;
      } catch (error) {
        console.error('Ошибка при получении отделов:', error);
        this.accessLevels = [];
      }
    },
    
    // Получение списка моделей LLM
    async fetchLLMModels() {
      try {
        const response = await axios.get('http://192.168.81.149:8000/models/llm');
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
        const response = await axios.get('http://192.168.81.149:8000/models/embedding');
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
        const response = await axios.get('http://192.168.81.149:8000/tags');
        this.tags = response.data.tags;
      } catch (error) {
        console.error('Ошибка при получении тегов:', error);
      }
    },
    
    // Получение списка всего контента
    async fetchAllContent() {
      try {
        const response = await axios.get('http://192.168.81.149:8000/content/all');
        this.contentList = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка контента:', error);
        this.contentList = [];
      }
    },
    
    // Регистрация пользователя
    async registerUser() {
      try {
        const response = await axios.post('http://192.168.81.149:8000/register', this.registerForm);
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
            !this.contentForm.access_level || !this.contentForm.file) {
          this.uploadMessage = 'Все поля должны быть заполнены';
          this.uploadStatus = false;
          return;
        }

        // Создаем объект FormData для отправки файла
        const formData = new FormData();
        formData.append('file', this.contentForm.file);
        
        // Отправляем запрос с параметрами в URL-строке
        const response = await axios.post(
          `http://192.168.81.149:8000/upload-content?title=${encodeURIComponent(this.contentForm.title)}` +
          `&description=${encodeURIComponent(this.contentForm.description)}` +
          `&access_id=${this.contentForm.access_level}` +
          `&department_id=${this.contentForm.department_id}` +
          `&tag_id=${this.contentForm.tag_id || ''}`,
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
          file: null
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
    
    // Инициализация LLM
    async initializeLLM() {
      if (!this.initializeForm.confirm) {
        this.initializeMessage = 'Пожалуйста, подтвердите инициализацию';
        this.initializeStatus = false;
        return;
      }
      
      this.isInitializing = true;
      this.initializeMessage = 'Идет инициализация LLM, это может занять некоторое время...';
      this.initializeStatus = true;
      
      try {
        // Удаляем лишние пробелы из значений
        const modelName = this.initializeForm.model_name.trim();
        const embeddingModelName = this.initializeForm.embedding_model_name.trim();
        const documentsPath = this.initializeForm.documents_path.trim();
        const departmentId = this.initializeForm.department_id.trim();
        
        // Проверяем, что departmentId не пустой
        if (!departmentId) {
          this.initializeMessage = 'ID отдела не может быть пустым';
          this.initializeStatus = false;
          this.isInitializing = false;
          return;
        }
        
        // Отладочная информация: выводим параметры, которые отправляем
        console.log('Отправляемые параметры:', {
          model_name: modelName,
          embedding_model_name: embeddingModelName,
          documents_path: documentsPath,
          department_id: departmentId
        });
        
        // Создаем объект данных для отправки в формате JSON
        const requestData = {
          model_name: modelName,
          embedding_model_name: embeddingModelName,
          documents_path: documentsPath,
          department_id: departmentId
        };
        
        // Отправляем запрос с JSON данными в теле запроса
        const response = await axios.post('http://192.168.81.149:8000/initialize', requestData);
        
        this.initializeMessage = 'LLM успешно инициализирован!';
        this.initializeStatus = true;
        
        // Сбрасываем подтверждение
        this.initializeForm.confirm = false;
      } catch (error) {
        this.initializeMessage = 'Ошибка инициализации LLM: ' + (error.response?.data?.detail || error.message);
        this.initializeStatus = false;
        console.error('Ошибка инициализации LLM:', error);
      } finally {
        this.isInitializing = false;
      }
    },
    
    // Загрузка контента для редактирования
    async loadContentForEdit() {
      if (!this.editForm.id) return;
      
      try {
        const response = await axios.get(`http://192.168.81.149:8000/content/${this.editForm.id}`);
        const content = response.data;
        
        this.editForm = {
          id: content.id,
          title: content.title,
          description: content.description,
          department_id: content.department_id,
          access_level: content.access_level,
          tag_id: content.tag_id || null
        };
      } catch (error) {
        console.error('Ошибка при загрузке контента для редактирования:', error);
        this.editMessage = 'Ошибка при загрузке контента';
        this.editStatus = false;
      }
    },
    
    // Редактирование контента
    async editContent() {
      try {
        const response = await axios.put(`http://192.168.81.149:8000/content/${this.editForm.id}`, {
          title: this.editForm.title,
          description: this.editForm.description,
          access_id: this.editForm.access_level,
          department_id: this.editForm.department_id,
          tag_id: this.editForm.tag_id
        });
        
        this.editMessage = 'Контент успешно отредактирован!';
        this.editStatus = true;
        
        // Обновляем список контента
        await this.fetchAllContent();
        
        // Обновляем таблицу контента
        const contentTableRef = this.$refs.contentTable;
        if (contentTableRef && typeof contentTableRef.fetchAllContent === 'function') {
          contentTableRef.fetchAllContent();
        }
      } catch (error) {
        this.editMessage = error.response?.data?.detail || 'Ошибка при редактировании контента';
        this.editStatus = false;
        console.error('Ошибка редактирования контента:', error);
      }
    },
    
    // Создание нового теста/анкеты
    async createQuiz() {
      try {
        const response = await axios.post('http://192.168.81.149:8000/quiz/create', this.quizForm);
        this.quizMessage = 'Тест/анкета успешно создана!';
        this.quizStatus = true;
        
        // Очистка формы
        this.quizForm = {
          title: '',
          description: '',
          is_test: false,
          department_id: null,
          access_level: null,
          questions: []
        };
        
        // Обновляем список тестов/анкет
        await this.fetchQuizzes();
      } catch (error) {
        this.quizMessage = error.response?.data?.detail || 'Ошибка при создании теста/анкеты';
        this.quizStatus = false;
        console.error('Ошибка создания теста/анкеты:', error);
      }
    },
    
    // Получение списка тестов/анкет
    async fetchQuizzes() {
      this.loadingQuizzes = true;
      this.quizzesError = '';
      this.quizzes = [];
      
      try {
        // Получаем текущего пользователя
        const currentUser = JSON.parse(localStorage.getItem('user')) || {};
        const userId = currentUser.id || 1; // Используем ID 1 по умолчанию для администратора
        
        // Формируем параметры запроса
        let params = { user_id: userId };
        if (this.quizFilter.type !== 'all') {
          params.is_test = this.quizFilter.type === 'test';
        }
        if (this.quizFilter.department !== 'all') {
          params.department_id = this.quizFilter.department;
        }
        
        const response = await axios.get('http://192.168.81.149:8000/quiz/list', { params });
        this.quizzes = response.data;
      } catch (error) {
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
        // Получаем текущего пользователя
        const currentUser = JSON.parse(localStorage.getItem('user')) || {};
        const userId = currentUser.id || 1; // Используем ID 1 по умолчанию для администратора
        
        const response = await axios.get(`http://192.168.81.149:8000/quiz/${id}?user_id=${userId}`);
        this.selectedQuiz = response.data;
        // Открываем модальное окно
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
          const response = await axios.delete(`http://192.168.81.149:8000/quiz/${id}`);
          this.quizMessage = 'Тест/анкета успешно удалена!';
          this.quizStatus = true;
          
          // Обновляем список тестов/анкет
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
        const response = await axios.get(`http://192.168.81.149:8000/quiz/stats/${this.resultsQuizId}`);
        this.quizStatistics = response.data;
        
        // Получаем попытки пользователей
        // Если выбран конкретный пользователь
        if (this.resultsUserId) {
          await this.fetchUserAttempts();
        } else {
          // Получаем все попытки для теста
          const userAttemptsResponse = await axios.get(`http://192.168.81.149:8000/quiz/attempts?quiz_id=${this.resultsQuizId}`);
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
        let url = `http://192.168.81.149:8000/quiz/attempts/${this.resultsUserId}`;
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
        // Получаем текущего пользователя
        const currentUser = JSON.parse(localStorage.getItem('user')) || {};
        const userId = currentUser.id || 1; // Используем ID 1 по умолчанию для администратора
        
        const response = await axios.get(`http://192.168.81.149:8000/quiz/attempt/${id}?user_id=${userId}`);
        this.selectedAttempt = response.data;
        // Открываем модальное окно
        this.attemptDetailsModal.show();
      } catch (error) {
        this.attemptDetailsError = error.response?.data?.detail || 'Ошибка при получении деталей попытки';
      } finally {
        this.loadingAttemptDetails = false;
      }
    },
    
    // Методы для работы с вопросами и вариантами ответов
    addQuestion() {
      this.quizForm.questions.push({
        text: '',
        question_type: 'single_choice',
        options: [
          { id: 1, text: '' },
          { id: 2, text: '' }
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
        : 1;
      
      question.options.push({
        id: newId,
        text: ''
      });
      
      if (question.question_type === 'multiple_choice' && !Array.isArray(question.correct_answer)) {
        question.correct_answer = [];
      }
    },
    
    removeOption(question, index) {
      // Если удаляемый вариант был выбран как правильный, сбрасываем правильный ответ
      const optionId = question.options[index].id;
      
      if (question.question_type === 'single_choice' && question.correct_answer === optionId) {
        question.correct_answer = '';
      } else if (question.question_type === 'multiple_choice' && Array.isArray(question.correct_answer)) {
        question.correct_answer = question.correct_answer.filter(id => id !== optionId);
      }
      
      question.options.splice(index, 1);
    },
    
    // Обработка изменения типа вопроса
    handleQuestionTypeChange(question) {
      // Сбрасываем правильный ответ при изменении типа вопроса
      if (question.question_type === 'single_choice') {
        question.correct_answer = '';
      } else if (question.question_type === 'multiple_choice') {
        question.correct_answer = [];
      } else if (question.question_type === 'text') {
        question.correct_answer = '';
      }
      
      // Если тип вопроса не предполагает варианты, но они есть, сохраняем их на всякий случай
      if (question.question_type === 'text' && (!question.options || question.options.length === 0)) {
        question.options = [
          { id: 1, text: '' },
          { id: 2, text: '' }
        ];
      }
    },
    
    // Вспомогательные методы для отображения данных
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
        // Преобразуем к строке для корректного сравнения
        return String(question.correct_answer) === String(optionId);
      } else if (question.question_type === 'multiple_choice' && Array.isArray(question.correct_answer)) {
        // Преобразуем к строке для корректного сравнения
        return question.correct_answer.map(String).includes(String(optionId));
      }
      
      return false;
    },
    
    getQuestionText(questionId) {
      if (!this.selectedQuiz) return '';
      
      const question = this.selectedQuiz.questions.find(q => q.id === questionId);
      return question ? question.text : '';
    },
    
    getCorrectAnswerText(questionId) {
      if (!this.selectedQuiz) return '';
      
      const question = this.selectedQuiz.questions.find(q => q.id === questionId);
      if (!question || !question.correct_answer) return '';
      
      if (question.question_type === 'single_choice') {
        const option = question.options.find(o => o.id === question.correct_answer);
        return option ? option.text : '';
      } else if (question.question_type === 'multiple_choice' && Array.isArray(question.correct_answer)) {
        const selectedOptions = question.options.filter(o => question.correct_answer.includes(o.id));
        return selectedOptions.map(o => o.text).join(', ');
      }
      
      return question.correct_answer;
    },
    
    formatAnswerText(answer) {
      if (!answer || !answer.answer) return '-';
      
      const question = this.selectedQuiz.questions.find(q => q.id === answer.question_id);
      if (!question) return JSON.stringify(answer.answer);
      
      if (question.question_type === 'single_choice') {
        const option = question.options.find(o => o.id === answer.answer);
        return option ? option.text : answer.answer;
      } else if (question.question_type === 'multiple_choice' && Array.isArray(answer.answer)) {
        const selectedOptions = question.options.filter(o => answer.answer.includes(o.id));
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
        const response = await axios.get('http://192.168.81.149:8000/users');
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
  border-bottom: 2px solid #17c1e8;
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
</style>
