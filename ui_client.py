import streamlit as st
import os
import requests

# Настройки API
API_URL = "http://localhost:8000"  # Убедитесь, что этот URL соответствует вашему API

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