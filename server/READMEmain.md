# README

<p align="center">
    <img src="images/image.png" alt="Скриншот веб-интерфейса Streamlit" width="600">
</p>


Thank you very much to [amscotti](https://github.com/amscotti) whose repository I used as a basis. Thanks to him, I was able to implement this code



## Требования
- [Ollama](https://ollama.ai/) версия 0.5.7 или выше.
- [Python] версия 3.13 или выше.


## Установка
1. Клонируемся через------------------>`git clone`
2. В терминале------------------------>`python -m venv .venv`
3. Устанавливаем зависимости---------->`pip install requirements.txt`
4. Устанавливаем модели с помощью----->`ollama pull <Название модели>`


## Запуск
1. Запускаем СЕРВЕР------------------->`uvicorn app:app --host 192.168.81.10 --port 8000` 
2. Запускаем ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ--->`streamlit run ui_client.py`


{
  "model_name": "ilyagusev/saiga_llama3:latest",
  "embedding_model_name": "snowflake-arctic-embed2:latest",
  "documents_path": "Research"
}


## Используемые технологии
- [Langchain](https://github.com/langchain/langchain): Библиотека Python для работы с большими языковыми моделями.
- [Ollama](https://ollama.ai/): Платформа для запуска больших языковых моделей локально.
- [Chroma](https://docs.trychroma.com/): Векторная база данных для хранения и извлечения встраиваний.
- [PyPDF](https://pypi.org/project/PyPDF2/): Библиотека Python для чтения и манипуляции PDF файлами.
- [Streamlit](https://streamlit.io/): Веб-фреймворк для создания интерактивных приложений для проектов в области машинного обучения и науки о данных.
- [UV](https://astral.sh/uv): Быстрый и эффективный установщик и резольвер пакетов Python.






{
  "model_name": "ilyagusev/saiga_llama3:latest",
  "embedding_model_name": "snowflake-arctic-embed2:latest",
  "documents_path": "Research",
  "department_id": "5"
}


{
  "title": "Опрос о предпочтениях в программировании",
  "description": "Этот опрос поможет нам понять ваши предпочтения в области программирования.",
  "is_test": false,
  "department_id": 5,
  "access_level": 3,
  "questions": [
    {
      "text": "Какой язык программирования вы предпочитаете?",
      "question_type": "single_choice",
      "options": [
        {"id": 1, "text": "Python"},
        {"id": 2, "text": "Java"},
        {"id": 3, "text": "JavaScript"},
        {"id": 4, "text": "C++"}
      ],
      "correct_answer": "1",
      "order": 1
    },
    {
      "text": "Какой фреймворк вы используете чаще всего?",
      "question_type": "single_choice",
      "options": [
        {"id": 1, "text": "Django"},
        {"id": 2, "text": "Flask"},
        {"id": 3, "text": "Spring"},
        {"id": 4, "text": "React"}
      ],
      "correct_answer": "1",
      "order": 2
    },
    {
      "text": "Какой тип разработки вам больше нравится?",
      "question_type": "multiple_choice",
      "options": [
        {"id": 1, "text": "Веб-разработка"},
        {"id": 2, "text": "Мобильная разработка"},
        {"id": 3, "text": "Разработка игр"},
        {"id": 4, "text": "Научные вычисления"}
      ],
      "correct_answer": ["1", "2"],
      "order": 3
    },
    {
      "text": "Какой инструмент для контроля версий вы используете?",
      "question_type": "single_choice",
      "options": [
        {"id": 1, "text": "Git"},
        {"id": 2, "text": "SVN"},
        {"id": 3, "text": "Mercurial"},
        {"id": 4, "text": "Не использую"}
      ],
      "correct_answer": "1",
      "order": 4
    },
    {
      "text": "Как часто вы изучаете новые технологии?",
      "question_type": "single_choice",
      "options": [
        {"id": 1, "text": "Каждый день"},
        {"id": 2, "text": "Несколько раз в неделю"},
        {"id": 3, "text": "Несколько раз в месяц"},
        {"id": 4, "text": "Редко"}
      ],
      "correct_answer": "1",
      "order": 5
    },
    {
      "text": "Какой метод разработки вы предпочитаете?",
      "question_type": "single_choice",
      "options": [
        {"id": 1, "text": "Agile"},
        {"id": 2, "text": "Waterfall"},
        {"id": 3, "text": "Scrum"},
        {"id": 4, "text": "Kanban"}
      ],
      "correct_answer": "1",
      "order": 6
    },
    {
      "text": "Какой тип базы данных вы предпочитаете?",
      "question_type": "single_choice",
      "options": [
        {"id": 1, "text": "SQL"},
        {"id": 2, "text": "NoSQL"},
        {"id": 3, "text": "In-memory"},
        {"id": 4, "text": "Не использую базы данных"}
      ],
      "correct_answer": "1",
      "order": 7
    },
    {
      "text": "Какой подход к тестированию вы используете?",
      "question_type": "multiple_choice",
      "options": [
        {"id": 1, "text": "Юнит-тестирование"},
        {"id": 2, "text": "Интеграционное тестирование"},
        {"id": 3, "text": "Системное тестирование"},
        {"id": 4, "text": "Не тестирую"}
      ],
      "correct_answer": ["1", "2"],
      "order": 8
    },
    {
      "text": "Какой инструмент для управления проектами вы используете?",
      "question_type": "single_choice",
      "options": [
        {"id": 1, "text": "Jira"},
        {"id": 2, "text": "Trello"},
        {"id": 3, "text": "Asana"},
        {"id": 4, "text": "Не использую"}
      ],
      "correct_answer": "1",
      "order": 9
    },
    {
      "text": "Какой тип обучения вы предпочитаете?",
      "question_type": "single_choice",
      "options": [
        {"id": 1, "text": "Онлайн-курсы"},
        {"id": 2, "text": "Книги"},
        {"id": 3, "text": "Вебинары"},
        {"id": 4, "text": "Личное обучение"}
      ],
      "correct_answer": "1",
      "order": 10
    }
  ]
}




mysqldump -h [ip] -P [port] -u [user_name] -p [db_name] > [file_name.sql]
