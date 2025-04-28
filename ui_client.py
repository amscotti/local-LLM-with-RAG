import streamlit as st
import os
import requests
import subprocess
import threading
import time
import signal
import atexit

# Запуск API сервера в отдельном потоке
def start_api_server():
    global api_process
    api_process = subprocess.Popen(
        ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return api_process

# Остановка API сервера при завершении работы
def stop_api_server():
    if 'api_process' in globals() and api_process.poll() is None:
        os.kill(api_process.pid, signal.SIGTERM)
        print("API сервер остановлен.")

# Запуск API сервера перед инициализацией интерфейса
api_process = start_api_server()
atexit.register(stop_api_server)

# Даем серверу немного времени для запуска
time.sleep(3)

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