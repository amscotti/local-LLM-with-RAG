import streamlit as st

# Определяем страницы
page_0 = st.Page("pages/user_guide.py", title="Руководство пользователя")
page_1 = st.Page("pages/ui_client.py", title="Режим консультанта")
page_2 = st.Page("pages/generate.py", title="Генерация")
page_3 = st.Page("pages/admin.py", title="Админка")

# Настраиваем навигацию
pg = st.navigation([page_0, page_1, page_2, page_3])

# Запускаем выбранную страницу
pg.run()

