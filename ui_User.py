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

st.title("Интерфейс для Local LLM с RAG")

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

# Инициализация состояния для чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение сообщений чата из истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Чат интерфейс
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
