import streamlit as st
import os
import requests

# Настройки API
API_URL = "http://localhost:8000"  # Убедитесь, что этот URL соответствует вашему API

st.title("Чат с Saiga LLaMA 3 🦙")

# Раздел для загрузки файлов
st.header("Загрузка файлов")
uploaded_files = st.file_uploader("Выберите файлы для загрузки", accept_multiple_files=True)

if st.button("Загрузить файлы"):
    if uploaded_files:
        for file in uploaded_files:
            response = requests.post(f"{API_URL}/upload-file", files={"file": file})
            st.success(response.json().get("message"))
    else:
        st.warning("Пожалуйста, выберите файлы для загрузки.")

# Инициализация модели при первом запуске
if "model_initialized" not in st.session_state:
    with st.spinner("Инициализация модели..."):
        response = requests.post(f"{API_URL}/initialize", json={
            "model_name": "ilyagusev/saiga_llama3:latest",
            "embedding_model_name": "snowflake-arctic-embed2:latest",
            "documents_path": "Research"
        })
        if response.status_code == 200:
            st.session_state["model_initialized"] = True
            st.success("Модель успешно инициализирована!")
        else:
            st.error(f"Ошибка инициализации модели: {response.json().get('detail')}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
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