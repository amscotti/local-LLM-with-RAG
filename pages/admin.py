import streamlit as st
import os
import requests

from langchain_ollama import ChatOllama
from document_loader import load_documents_into_database

from models import get_list_of_models

from llm import getStreamingChain


EMBEDDING_MODEL = "nomic-embed-text"
PATH = "Research"

# Настройки API
API_URL = "http://localhost:8000"  # Убедитесь, что этот URL соответствует вашему API

# Проверяем, нужно ли перенаправить на админку
if "redirect_to_admin" not in st.session_state:
    st.session_state.redirect_to_admin = False

# Если нужно перенаправить, показываем админку
if st.session_state.redirect_to_admin:
    # Проверка пароля
    if "authenticated" not in st.session_state:
        password = st.text_input("Введите пароль для доступа к админке", type="password")
        if st.button("Войти"):
            if password == "123":  # Замените "123" на желаемый пароль
                st.session_state.authenticated = True
                st.success("Доступ к админке предоставлен!")
            else:
                st.error("Неверный пароль. Попробуйте снова.")
    else:
        st.title("Админка")
        
        # Добавляем навигацию в боковую панель
        st.sidebar.markdown("### Навигация")
        st.sidebar.markdown("[Главная страница](/)")
        st.sidebar.markdown("[Генерация без RAG](/generate)")
        
        # Инициализация списка моделей
        if "list_of_models" not in st.session_state:
            st.session_state["list_of_models"] = get_list_of_models()

        # Раздел для загрузки файлов
        st.header("Загрузка файлов")
        uploaded_files = st.file_uploader("Выберите файлы для загрузки", accept_multiple_files=True)

        if st.button("Загрузить файлы"):
            if uploaded_files:
                for file in uploaded_files:
                    response = requests.post(f"{API_URL}/upload-files", files={"files": file})
                    st.success(response.json().get("message"))
            else:
                st.warning("Пожалуйста, выберите файлы для загрузки.")

        # Раздел для инициализации модели
        st.header("Инициализация модели")
        selected_model = st.selectbox("Выберите модель", st.session_state["list_of_models"], index=0)
        embedding_model_name = st.text_input("Имя модели встраивания", "snowflake-arctic-embed2:latest")
        documents_path = st.text_input("Путь к документам", "Research")

        if st.button("Инициализировать модель"):
            response = requests.post(f"{API_URL}/initialize", json={
                "model_name": selected_model,
                "embedding_model_name": embedding_model_name,
                "documents_path": documents_path
            })
            if response.status_code == 200:
                st.success(response.json().get("message"))
            else:
                st.error(response.json().get("detail"))

        # Раздел для запроса к модели
        st.header("Запрос к модели")
        user_question = st.text_input("Введите ваш вопрос")

        if st.button("Отправить вопрос"):
            response = requests.post(f"{API_URL}/query", json={"question": user_question})
            if response.status_code == 200:
                answer = response.json().get("answer")
                chunks = response.json().get("chunks")
                files = response.json().get("files")
                st.success(f"Ответ: {answer}")
                st.write("Фрагменты:", chunks)
                st.write("Файлы:", files)
            else:
                st.error(response.json().get("detail"))

        if st.session_state.get("ollama_model") != selected_model:
            st.session_state["ollama_model"] = selected_model
            st.session_state["llm"] = ChatOllama(model=selected_model)

        # Initialize states
        if "db" not in st.session_state:
            st.session_state.db = None

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        # Удалено лишнее поле st.chat_input("Вопрос"), используем только "Введите ваш вопрос"
        if user_question:  # Используем переменную user_question из предыдущего кода
            st.session_state.messages.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):
                stream = getStreamingChain(
                    user_question,
                    st.session_state.messages,
                    st.session_state.llm,
                    st.session_state.db,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.title("База знаний НПО \"СПЕКТРОН\"", anchor=None)

    # Добавляем кнопку для перехода в админку
    st.sidebar.markdown("[Перейти в админку](/admin)", unsafe_allow_html=True)

    # Инициализируем историю чата
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Отображаем сообщения из истории при перезапуске приложения
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Чат-интерфейс
    if prompt := st.chat_input("Задайте вопрос..."):
        # Добавляем сообщение пользователя в историю
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Отображаем сообщение пользователя
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Отправляем запрос и отображаем ответ
        with st.chat_message("assistant"):
            with st.spinner("Генерирую ответ..."):
                response = requests.post(f"{API_URL}/query", json={"question": prompt})
                if response.status_code == 200:
                    answer = response.json().get("answer")
                    st.markdown(answer)
                    # Добавляем ответ ассистента в историю
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Ошибка: {response.json().get('detail')}")

# Кнопка для перехода в админку
if st.button("Перейти в админку"):
    st.session_state.redirect_to_admin = True
