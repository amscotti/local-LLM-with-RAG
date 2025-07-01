/**
 * Утилита для централизованного логирования ошибок
 */

// Максимальное количество ошибок для хранения в localStorage
const MAX_ERRORS_STORED = 50;

// Ключ для хранения ошибок в localStorage
const ERROR_STORAGE_KEY = 'app_error_logs';

/**
 * Логирует ошибку в консоль и сохраняет в localStorage
 * @param {Error|string} error - Объект ошибки или сообщение об ошибке
 * @param {string} source - Источник ошибки (компонент, модуль и т.д.)
 * @param {Object} context - Дополнительный контекст ошибки
 */
export const logError = (error, source = 'unknown', context = {}) => {
  // Форматируем ошибку
  const errorObj = {
    message: error instanceof Error ? error.message : String(error),
    stack: error instanceof Error ? error.stack : null,
    source,
    context,
    timestamp: new Date().toISOString(),
    url: window.location.href
  };
  
  // Логируем в консоль
  console.error(`[${source}] ${errorObj.message}`, error, context);
  
  // Сохраняем в localStorage
  try {
    let errors = JSON.parse(localStorage.getItem(ERROR_STORAGE_KEY) || '[]');
    
    // Добавляем новую ошибку в начало массива
    errors.unshift(errorObj);
    
    // Ограничиваем количество хранимых ошибок
    if (errors.length > MAX_ERRORS_STORED) {
      errors = errors.slice(0, MAX_ERRORS_STORED);
    }
    
    localStorage.setItem(ERROR_STORAGE_KEY, JSON.stringify(errors));
  } catch (e) {
    console.error('Не удалось сохранить ошибку в localStorage:', e);
  }
  
  // Здесь можно добавить отправку ошибки на сервер
  // sendErrorToServer(errorObj);
};

/**
 * Получает список сохраненных ошибок
 * @returns {Array} Массив объектов ошибок
 */
export const getStoredErrors = () => {
  try {
    return JSON.parse(localStorage.getItem(ERROR_STORAGE_KEY) || '[]');
  } catch (e) {
    console.error('Не удалось получить сохраненные ошибки:', e);
    return [];
  }
};

/**
 * Очищает список сохраненных ошибок
 */
export const clearStoredErrors = () => {
  try {
    localStorage.removeItem(ERROR_STORAGE_KEY);
  } catch (e) {
    console.error('Не удалось очистить сохраненные ошибки:', e);
  }
};

/**
 * Отправляет ошибку на сервер (заглушка)
 * @param {Object} errorObj - Объект ошибки
 */
const sendErrorToServer = (errorObj) => {
  // В реальном приложении здесь был бы код для отправки ошибки на сервер
  // Например, с использованием Sentry или собственного API
  
  // fetch('/api/log-error', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify(errorObj),
  // }).catch(e => console.error('Не удалось отправить ошибку на сервер:', e));
};

/**
 * Глобальный обработчик необработанных ошибок
 */
export const setupGlobalErrorHandlers = () => {
  // Обработка необработанных исключений
  window.addEventListener('error', (event) => {
    logError(event.error || event.message, 'window.onerror', {
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno
    });
  });
  
  // Обработка необработанных отклоненных промисов
  window.addEventListener('unhandledrejection', (event) => {
    logError(event.reason || 'Unhandled Promise Rejection', 'unhandledrejection', {
      promise: event.promise
    });
  });
  
  // Переопределение console.error для логирования всех ошибок
  const originalConsoleError = console.error;
  console.error = (...args) => {
    // Вызываем оригинальный метод
    originalConsoleError.apply(console, args);
    
    // Логируем только если первый аргумент - ошибка или строка
    if (args.length > 0 && (args[0] instanceof Error || typeof args[0] === 'string')) {
      // Избегаем рекурсии, проверяя, не вызвана ли console.error из logError
      const stack = new Error().stack || '';
      if (!stack.includes('logError')) {
        logError(args[0], 'console.error', { additionalArgs: args.slice(1) });
      }
    }
  };
}; 