/**
 * Утилита для параллельного выполнения запросов с использованием Promise.all
 */

import axiosInstance from './axiosConfig';
import { logError } from './errorLogger';

/**
 * Выполняет несколько запросов параллельно
 * @param {Array<Object>} requests - Массив объектов запросов
 * @param {Object} options - Дополнительные опции
 * @returns {Promise<Array>} - Массив результатов запросов
 * 
 * @example
 * // Пример использования:
 * const results = await executeParallelRequests([
 *   { url: '/users', method: 'get' },
 *   { url: '/quizzes', method: 'get', params: { limit: 10 } }
 * ]);
 */
export const executeParallelRequests = async (requests, options = {}) => {
  const {
    stopOnError = false,
    timeout = 30000,
    onProgress = null,
    retryCount = 1
  } = options;
  
  // Создаем массив промисов для каждого запроса
  const promises = requests.map((request, index) => {
    return new Promise((resolve, reject) => {
      // Добавляем таймаут для запроса
      const timeoutId = setTimeout(() => {
        reject(new Error(`Запрос ${request.url} превысил таймаут ${timeout}мс`));
      }, timeout);
      
      // Выполняем запрос с поддержкой повторных попыток
      const executeRequest = async (attempt = 0) => {
        try {
          const response = await axiosInstance(request);
          
          // Очищаем таймаут
          clearTimeout(timeoutId);
          
          // Вызываем колбэк прогресса, если он предоставлен
          if (onProgress) {
            onProgress(index, requests.length, response.data);
          }
          
          resolve(response.data);
        } catch (error) {
          // Пробуем повторить запрос, если не превышено количество попыток
          if (attempt < retryCount) {
            // Экспоненциальная задержка между попытками
            const delay = Math.pow(2, attempt) * 1000;
            console.warn(`Повторная попытка (${attempt + 1}/${retryCount}) для ${request.url} через ${delay}мс`);
            
            await new Promise(r => setTimeout(r, delay));
            return executeRequest(attempt + 1);
          }
          
          // Очищаем таймаут
          clearTimeout(timeoutId);
          
          // Логируем ошибку
          logError(error, 'parallelRequests', { request });
          
          reject(error);
        }
      };
      
      // Запускаем запрос
      executeRequest();
    });
  });
  
  // Выполняем все запросы параллельно
  if (stopOnError) {
    // Если stopOnError=true, используем Promise.all, который остановится при первой ошибке
    return Promise.all(promises);
  } else {
    // Иначе используем Promise.allSettled, который выполнит все запросы независимо от ошибок
    const results = await Promise.allSettled(promises);
    
    // Преобразуем результаты в более удобный формат
    return results.map((result, index) => {
      if (result.status === 'fulfilled') {
        return {
          success: true,
          data: result.value,
          error: null,
          request: requests[index]
        };
      } else {
        return {
          success: false,
          data: null,
          error: result.reason,
          request: requests[index]
        };
      }
    });
  }
};

/**
 * Загружает данные для инициализации компонента параллельно
 * @param {Array<Function>} loaders - Массив функций загрузки данных
 * @returns {Promise<Object>} - Объект с результатами загрузки
 * 
 * @example
 * // Пример использования:
 * const { quizzes, users, departments } = await loadComponentData([
 *   () => axios.get('/quizzes'),
 *   () => axios.get('/users'),
 *   () => axios.get('/departments')
 * ]);
 */
export const loadComponentData = async (loaders) => {
  try {
    // Выполняем все функции загрузки параллельно
    const results = await Promise.all(loaders.map(loader => loader()));
    
    // Возвращаем объект с результатами
    return results.reduce((acc, result, index) => {
      // Используем индекс как ключ, если имя не предоставлено
      const key = loaders[index].name || `data${index}`;
      acc[key] = result.data || result;
      return acc;
    }, {});
  } catch (error) {
    logError(error, 'loadComponentData');
    throw error;
  }
};

/**
 * Загружает данные с поддержкой частичных результатов
 * @param {Object} requests - Объект с функциями загрузки данных
 * @returns {Promise<Object>} - Объект с результатами загрузки
 * 
 * @example
 * // Пример использования:
 * const { quizzes, users, departments } = await loadPartialData({
 *   quizzes: () => axios.get('/quizzes'),
 *   users: () => axios.get('/users'),
 *   departments: () => axios.get('/departments')
 * });
 */
export const loadPartialData = async (requests) => {
  const keys = Object.keys(requests);
  const results = {};
  const errors = {};
  
  // Выполняем все запросы параллельно с помощью Promise.allSettled
  const promises = keys.map(key => requests[key]());
  const settledResults = await Promise.allSettled(promises);
  
  // Обрабатываем результаты
  settledResults.forEach((result, index) => {
    const key = keys[index];
    
    if (result.status === 'fulfilled') {
      results[key] = result.value.data || result.value;
    } else {
      errors[key] = result.reason;
      logError(result.reason, `loadPartialData:${key}`);
      // Устанавливаем пустой результат для этого ключа
      results[key] = null;
    }
  });
  
  // Добавляем информацию об ошибках в результат
  results._errors = errors;
  results._hasErrors = Object.keys(errors).length > 0;
  
  return results;
}; 