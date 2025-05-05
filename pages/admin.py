import streamlit as st
import requests
from models import get_list_of_models

# Настройки API
API_URL = "http://localhost:8000"  # Убедитесь, что этот URL соответствует вашему API

# Проверяем, нужно ли перенаправить на админку
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