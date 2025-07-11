/**
 * Утилита для централизованного логирования ошибок
 */

// Максимальное количество ошибок для хранения в localStorage
const MAX_ERRORS_STORED = 50;

// Ключ для хранения ошибок в localStorage
const ERROR_STORAGE_KEY = 'app_error_logs';

// Счетчик ошибок для предотвращения рекурсивных вызовов
let errorCount = 0;
const ERROR_THRESHOLD = 100; // Максимальное количество ошибок в короткий промежуток времени
const ERROR_RESET_INTERVAL = 5000; // Интервал сброса счетчика ошибок (5 секунд)
let lastErrorTime = 0;
let isProcessingError = false;

/**
 * Логирует ошибку в консоль и сохраняет в localStorage
 * @param {Error|string} error - Объект ошибки или сообщение об ошибке
 * @param {string} source - Источник ошибки (компонент, модуль и т.д.)
 * @param {Object} context - Дополнительный контекст ошибки
 */
export const logError = (error, source = 'unknown', context = {}) => {
  // Проверка на слишком частые вызовы
  const now = Date.now();
  if (now - lastErrorTime > ERROR_RESET_INTERVAL) {
    errorCount = 0;
    lastErrorTime = now;
  }
  
  // Проверка на превышение порога ошибок
  if (errorCount > ERROR_THRESHOLD) {
    if (errorCount === ERROR_THRESHOLD + 1) {
      const originalConsoleError = console.__originalError || console.error;
      originalConsoleError.call(console, `[errorLogger] Слишком много ошибок (${ERROR_THRESHOLD}+), логирование временно приостановлено`);
    }
    errorCount++;
    return;
  }
  
  // Защита от рекурсивных вызовов
  if (isProcessingError) {
    return;
  }
  
  isProcessingError = true;
  errorCount++;
  
  try {
    // Форматируем ошибку
    const errorObj = {
      message: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : null,
      source,
      context,
      timestamp: new Date().toISOString(),
      url: window.location.href
    };
    
    // Логируем в консоль через оригинальный метод
    const originalConsoleError = console.__originalError || console.error;
    originalConsoleError.call(console, `[${source}] ${errorObj.message}`, error, context);
    
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
      // Используем оригинальный console.error для избежания рекурсии
      originalConsoleError.call(console, 'Не удалось сохранить ошибку в localStorage:', e);
    }
    
    // Здесь можно добавить отправку ошибки на сервер
    // sendErrorToServer(errorObj);
  } finally {
    isProcessingError = false;
  }
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
  
  // Сохраняем оригинальный console.error
  console.__originalError = console.error;
  
  // Переопределение console.error для логирования всех ошибок
  console.error = (...args) => {
    // Вызываем оригинальный метод напрямую
    console.__originalError.apply(console, args);
    
    // Логируем только если первый аргумент - ошибка или строка и не превышен порог ошибок
    if (args.length > 0 && (args[0] instanceof Error || typeof args[0] === 'string') && errorCount <= ERROR_THRESHOLD) {
      // Избегаем рекурсии, проверяя, не вызвана ли console.error из logError
      const stack = new Error().stack || '';
      if (!stack.includes('logError') && !isProcessingError) {
        logError(args[0], 'console.error', { additionalArgs: args.slice(1) });
      }
    }
  };
  
  // Сбрасываем счетчик ошибок периодически
  setInterval(() => {
    if (errorCount > 0) {
      errorCount = 0;
      console.__originalError.call(console, `[errorLogger] Счетчик ошибок сброшен`);
    }
  }, ERROR_RESET_INTERVAL);
}; 