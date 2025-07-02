import http from 'k6/http';
import { sleep, check, group } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';
import { SharedArray } from 'k6/data';

// Настраиваемые метрики
const endpointErrors = new Counter('endpoint_errors');
const endpointRequests = new Counter('endpoint_requests');
const successRate = new Rate('success_rate');
const responseTimes = new Trend('response_times');
const chatRequests = new Counter('chat_requests');
const feedbackRequests = new Counter('feedback_requests');

// Количество пользователей задается через переменную окружения
export let options = {
  scenarios: {
    contacts: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: __ENV.USERS || 50 },  // Разогрев до указанного числа пользователей
        { duration: '2m', target: __ENV.USERS || 50 },   // Поддерживаем указанное число пользователей
        { duration: '30s', target: 0 },                  // Постепенное завершение
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],   // Менее 5% запросов должны завершиться неудачно
    http_req_duration: ['p(95)<3000'], // 95% запросов должны завершиться менее чем за 3 секунды
    'success_rate': ['rate>0.95'],     // Успешность выполнения должна быть выше 95%
    'endpoint_errors': ['count<100'],  // Не более 100 ошибок за весь тест
  },
};

// Базовый URL API через Nginx
const baseUrl = 'http://192.168.81.10:8081/api';

// Примеры вопросов для чата
const chatQuestions = [
  'Как работает система обратной связи?',
  'Какие документы доступны в системе?',
  'Как добавить новый контент?',
  'Какие теги используются чаще всего?',
  'Как получить доступ к закрытым документам?',
  'Какие отделы представлены в системе?',
  'Как обновить свой профиль?',
  'Какие форматы файлов поддерживаются?',
  'Как работает поиск по документам?',
  'Как создать новый тег?'
];

// Примеры текстов для обратной связи
const feedbackTexts = [
  'Хотелось бы больше функций для работы с документами',
  'Система работает отлично, спасибо за разработку!',
  'Обнаружил ошибку при загрузке файлов большого размера',
  'Предлагаю добавить возможность экспорта данных',
  'Интерфейс очень удобный, но хотелось бы больше настроек',
  'Не могу найти некоторые документы через поиск',
  'Чат с ИИ очень полезен, но иногда отвечает медленно',
  'Предлагаю улучшить систему тегов',
  'Хотелось бы иметь возможность группировать документы',
  'Как можно получить больше прав доступа к системе?'
];

// Функция для авторизации пользователя
function getAuthToken() {
  const payload = JSON.stringify({
    login: 'Pavel2',
    password: '123123'
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const loginRes = http.post(`${baseUrl}/user/login`, payload, params);
  
  if (loginRes.status === 200) {
    return loginRes.json().auth_key;
  }
  
  return null;
}

// Тестирование эндпоинта
function testEndpoint(token, endpoint, method = 'GET', data = null) {
  endpointRequests.add(1);
  
  const url = `${baseUrl}${endpoint}`;
  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  // Добавляем токен авторизации, если он есть
  if (token) {
    params.headers['Authorization'] = `Bearer ${token}`;
  }
  
  const startTime = new Date();
  let response;
  
  // Выполняем запрос в зависимости от метода
  switch(method.toUpperCase()) {
    case 'GET':
      response = http.get(url, params);
      break;
    case 'POST':
      response = http.post(url, data ? JSON.stringify(data) : '', params);
      break;
    case 'PUT':
      response = http.put(url, data ? JSON.stringify(data) : '', params);
      break;
    case 'DELETE':
      response = http.del(url, null, params);
      break;
    default:
      response = http.get(url, params);
  }
  
  // Измеряем время ответа
  const responseTime = new Date() - startTime;
  responseTimes.add(responseTime);
  
  // Проверяем успешность запроса
  const success = check(response, {
    'status is 200': (r) => r.status === 200,
    'response is valid': (r) => r.status < 400,
  });
  
  successRate.add(success);
  
  if (!success) {
    endpointErrors.add(1);
    console.log(`Ошибка при запросе к ${url}: ${response.status} ${response.body}`);
  }
  
  return response;
}

// Отправка запроса в чат ИИ
function sendChatRequest(token) {
  chatRequests.add(1);
  
  // Выбираем случайный вопрос из списка
  const randomQuestion = chatQuestions[Math.floor(Math.random() * chatQuestions.length)];
  
  const chatData = {
    question: randomQuestion,
    department_id: "1" // Предполагаем, что это валидный ID отдела
  };
  
  const chatResponse = testEndpoint(token, '/llm/query', 'POST', chatData);
  
  if (chatResponse.status === 200) {
    check(chatResponse, {
      'has answer': (r) => r.json().hasOwnProperty('answer'),
      'answer not empty': (r) => r.json().answer && r.json().answer.length > 0,
    });
  }
  
  // Пауза после запроса к чату
  sleep(1);
}

// Отправка запроса обратной связи
function sendFeedbackRequest(token, userId) {
  feedbackRequests.add(1);
  
  // Выбираем случайный текст из списка
  const randomText = feedbackTexts[Math.floor(Math.random() * feedbackTexts.length)];
  
  // Для обратной связи используем FormData
  const formData = new FormData();
  formData.append('user_id', userId || '1'); // Используем ID пользователя из токена или дефолтный
  formData.append('text', randomText);
  
  // Для простоты не добавляем фото в тесте
  
  const feedbackResponse = http.post(
    `${baseUrl}/feedback/create`, 
    formData, 
    {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      }
    }
  );
  
  if (feedbackResponse.status === 200) {
    check(feedbackResponse, {
      'feedback created': (r) => r.json().hasOwnProperty('message'),
      'has feedback id': (r) => r.json().hasOwnProperty('feedback_id'),
    });
  }
  
  // Пауза после запроса обратной связи
  sleep(1);
}

// Основная функция теста
export default function() {
  // Получаем токен авторизации один раз для каждого виртуального пользователя
  const token = getAuthToken();
  const userId = '1'; // Предполагаем, что это валидный ID пользователя
  
  // Определяем, какой тип запроса будет выполнять этот пользователь (50/50)
  const isChatUser = Math.random() < 0.5;
  
  if (isChatUser) {
    // 50% пользователей отправляют запросы в чат ИИ
    group('Chat Endpoint', function() {
      sendChatRequest(token);
    });
  } else {
    // 50% пользователей отправляют обратную связь
    group('Feedback Endpoint', function() {
      sendFeedbackRequest(token, userId);
    });
  }
  
  // Небольшая пауза между итерациями теста
  sleep(Math.random() * 2 + 1);
}

// Функция для выполнения перед началом теста
export function setup() {
  console.log(`Начало тестирования с ${__ENV.USERS || 50} пользователями`);
  console.log('50% пользователей будут отправлять запросы в чат ИИ');
  console.log('50% пользователей будут отправлять обратную связь');
  return { startTime: new Date() };
}

// Функция для выполнения после завершения теста
export function teardown(data) {
  const testDuration = (new Date() - data.startTime) / 1000;
  console.log(`Тест завершен. Продолжительность: ${testDuration} секунд`);
  console.log(`Всего запросов к чату: ${chatRequests.count}`);
  console.log(`Всего запросов обратной связи: ${feedbackRequests.count}`);
} 