import axios from 'axios';

// Создаем экземпляр Axios с базовой конфигурацией
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 15000, // 15 секунд таймаут для запросов
  headers: {
    'Content-Type': 'application/json',
  }
});

// Максимальное количество повторных попыток
const MAX_RETRIES = 3;

// Хранилище для отслеживания повторных попыток
const retryStorage = new Map();

// Перехватчик запросов
axiosInstance.interceptors.request.use(
  config => {
    // Добавляем информацию о попытке запроса
    const requestId = `${config.method}-${config.url}-${Date.now()}`;
    config.requestId = requestId;
    
    // Получаем токен из localStorage
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Добавляем userId как параметр запроса, если он есть в localStorage и еще не добавлен
    const userId = localStorage.getItem('userId');
    if (userId) {
      // Инициализируем params, если их нет
      if (!config.params) {
        config.params = {};
      }
      
      // Добавляем user_id только если его еще нет в параметрах и URL не содержит user_id в пути
      if (!config.params.user_id && !config.url.includes(`/user/${userId}/`)) {
        config.params.user_id = userId;
      }
    }
    
    // Логируем запрос в консоль в режиме разработки
    if (import.meta.env.DEV) {
      console.log(`🚀 Запрос: ${config.method?.toUpperCase()} ${config.url}`, config);
    }
    
    return config;
  },
  error => {
    console.error('❌ Ошибка при создании запроса:', error);
    return Promise.reject(error);
  }
);

// Перехватчик ответов
axiosInstance.interceptors.response.use(
  response => {
    // Логируем успешный ответ в режиме разработки
    if (import.meta.env.DEV) {
      console.log(`✅ Ответ: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data);
    }
    
    // Очищаем информацию о повторных попытках для этого запроса
    if (response.config.requestId) {
      retryStorage.delete(response.config.requestId);
    }
    
    return response;
  },
  async error => {
    const originalConfig = error.config;
    
    // Если нет конфигурации запроса или уже достигнуто максимальное количество попыток
    if (!originalConfig || !originalConfig.requestId) {
      return Promise.reject(error);
    }
    
    // Получаем текущее количество попыток
    const retryCount = retryStorage.get(originalConfig.requestId) || 0;
    
    // Проверяем, можем ли мы повторить запрос
    const canRetry = retryCount < MAX_RETRIES && (
      // Повторяем при ошибках сети
      error.message.includes('Network Error') ||
      // Повторяем при таймауте
      error.code === 'ECONNABORTED' ||
      // Повторяем при определенных HTTP-статусах
      (error.response && [408, 429, 500, 502, 503, 504].includes(error.response.status))
    );
    
    if (canRetry) {
      // Увеличиваем счетчик попыток
      retryStorage.set(originalConfig.requestId, retryCount + 1);
      
      // Экспоненциальная задержка между попытками (1s, 2s, 4s, ...)
      const delay = Math.pow(2, retryCount) * 1000;
      
      // Логируем информацию о повторной попытке
      console.warn(`🔄 Повторная попытка (${retryCount + 1}/${MAX_RETRIES}) для ${originalConfig.method?.toUpperCase()} ${originalConfig.url} через ${delay}ms`);
      
      // Ждем перед повторной попыткой
      await new Promise(resolve => setTimeout(resolve, delay));
      
      // Повторяем запрос
      return axiosInstance(originalConfig);
    }
    
    // Логируем ошибку
    if (error.response) {
      // Ошибка с ответом от сервера
      console.error(`❌ Ошибка ${error.response.status}: ${originalConfig.method?.toUpperCase()} ${originalConfig.url}`, 
        error.response.data);
      
      // Обработка ошибок аутентификации
      if (error.response.status === 401) {
        console.warn('🔑 Ошибка аутентификации, перенаправление на страницу входа');
        localStorage.removeItem('token');
        window.location.href = '/sign-in';
      }
    } else if (error.request) {
      // Запрос был сделан, но ответ не получен
      console.error('❌ Нет ответа от сервера:', error.request);
    } else {
      // Что-то пошло не так при настройке запроса
      console.error('❌ Ошибка запроса:', error.message);
    }
    
    // Очищаем информацию о повторных попытках
    retryStorage.delete(originalConfig.requestId);
    
    return Promise.reject(error);
  }
);

// Функция для кэширования ответов в localStorage
const cacheAdapter = () => {
  const cache = new Map();
  
  return async config => {
    // Кэшируем только GET-запросы
    if (config.method.toLowerCase() !== 'get' || config.noCache) {
      return axios(config);
    }
    
    // Создаем ключ кэша на основе URL и параметров
    const cacheKey = `${config.url}${JSON.stringify(config.params || {})}`;
    
    // Проверяем, есть ли данные в кэше
    const cachedData = cache.get(cacheKey);
    
    if (cachedData) {
      // Используем кэшированные данные
      console.log(`📦 Используются кэшированные данные для ${config.url}`);
      return Promise.resolve(cachedData);
    }
    
    // Если данных в кэше нет, выполняем запрос
    const response = await axios(config);
    
    // Сохраняем ответ в кэше
    cache.set(cacheKey, response);
    
    return response;
  };
};

// Экспортируем настроенный экземпляр Axios
export default axiosInstance; 