import requests
from bs4 import BeautifulSoup
import PyPDF2

def fetch_page(url: str) -> str:
    """Получает HTML-код страницы по указанному URL."""
    response = requests.get(url)
    response.raise_for_status()  # Проверка на ошибки
    return response.text

def parse_titles(html: str) -> list[str]:
    """Извлекает заголовки (h1) из HTML-кода."""
    soup = BeautifulSoup(html, 'html.parser')
    titles = [h1.get_text() for h1 in soup.find_all('h1')]
    return titles

def extract_text_from_pdf(pdf_path: str) -> str:
    """Извлекает текст из PDF-документа."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def main(url: str, pdf_path: str):
    """Основная функция для запуска парсера."""
    html = fetch_page(url)
    titles = parse_titles(html)
    print("Заголовки на странице:")
    for title in titles:
        print(title)
    text = extract_text_from_pdf(pdf_path)
    print("Извлеченный текст из PDF:")
    print(text)

if __name__ == "__main__":
    # Пример использования
    url = "https://example.com"  # Замените на нужный URL
    pdf_path = "example.pdf"  # Замените на путь к вашему PDF-документу
    main(url, pdf_path)
