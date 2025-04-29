import subprocess
import os
import sys

def run_in_terminal(command):
    if sys.platform.startswith('win'):
        # Для Windows
        subprocess.Popen(['start', 'cmd', '/k', command], shell=True)
    else:
        # Для Unix-подобных систем (Linux, macOS)
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])

if __name__ == "__main__":
    # Команды для запуска
    streamlit_command = "streamlit run ui_client.py"
    uvicorn_command = "uvicorn app:app --host 0.0.0.0 --port 8000"

    # Запуск команд в разных терминалах
    run_in_terminal(streamlit_command)
    run_in_terminal(uvicorn_command)
