import streamlit as st
import requests
from models import get_list_of_models

# Настройки API
API_URL = "http://localhost:8000"  # Убедитесь, что этот URL соответствует вашему API

st.title("Генерация без RAG")

# Инициализация списка моделей
if "list_of_models" not in st.session_state:
    st.session_state["list_of_models"] = get_list_of_models()

# Раздел для выбора модели
st.header("Параметры генерации")
selected_model = st.selectbox("Выберите модель", st.session_state["list_of_models"], index=0)

# Инициализируем историю чата
if "generate_messages" not in st.session_state:
    st.session_state.generate_messages = []

# Текстовая область для ввода запроса
user_input = st.text_area("Введите текст для генерации", height=200)

if st.button("Сгенерировать"):
    if user_input:
        with st.spinner("Генерация текста..."):
            # Отправляем запрос к API
            try:
                response = requests.post(f"{API_URL}/generate", json={
                    "messages": user_input,
                    "model": selected_model
                })
                
                if response.status_code == 200:
                    result_text = response.json().get("text")
                    model_used = response.json().get("model")
                    
                    # Добавляем сообщения в историю
                    st.session_state.generate_messages.append({"role": "user", "content": user_input})
                    st.session_state.generate_messages.append({"role": "assistant", "content": result_text})
                    
                    # Отображаем результат
                    st.success(f"Модель: {model_used}")
                    st.markdown("### Результат:")
                    st.markdown(result_text)
                else:
                    st.error(f"Ошибка: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Ошибка при отправке запроса: {str(e)}")
    else:
        st.warning("Пожалуйста, введите текст для генерации.")

# Отображаем историю генераций
if st.session_state.generate_messages:
    st.header("История генераций")
    for i in range(0, len(st.session_state.generate_messages), 2):
        if i+1 < len(st.session_state.generate_messages):
            with st.expander(f"Генерация {i//2 + 1}"):
                st.subheader("Запрос:")
                st.markdown(st.session_state.generate_messages[i]["content"])
                st.subheader("Ответ:")
                st.markdown(st.session_state.generate_messages[i+1]["content"])

# Кнопка для очистки истории
if st.session_state.generate_messages and st.button("Очистить историю"):
    st.session_state.generate_messages = []
    st.experimental_rerun()

# Добавляем навигацию
st.sidebar.markdown("### Навигация")
st.sidebar.markdown("[Главная страница](/)")
st.sidebar.markdown("[Админка](/admin)") 