from flask import Flask, request, Response
import requests
import logging
from urllib.parse import urljoin

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@app.route('/proxy/')
def proxy():
    target_url = request.args.get('url')
    
    if not target_url:
        app.logger.warning("Запрос без URL")
        return "URL is required", 400

    # Логирование поступившего URL
    app.logger.info(f"Received URL to proxy: {target_url}")

    # Убедитесь, что URL начинается с 'http://' или 'https://'
    if not target_url.startswith(('http://', 'https://')):
        app.logger.warning(f"Некорректный URL: {target_url}")
        return "Invalid URL: URL must start with 'http://' or 'https://'", 400

    try:
        # Прокси запрос на целевой URL
        response = requests.get(target_url)

        # Убираем заголовок X-Frame-Options из заголовков ответа
        headers = dict(response.headers)
        headers.pop('X-Frame-Options', None)

        # Переписывание путей к статическим ресурсам
        content = response.text
        base_url = target_url.rsplit('/', 1)[0] + '/'
        content = content.replace('src="/', f'src="{urljoin(base_url, "/")}')
        content = content.replace('href="/', f'href="{urljoin(base_url, "/")}')
        
        # Логирование успешного запроса
        app.logger.info(f"Successfully proxied request to: {target_url}")
        
        # Возвращение измененного контента обратно клиенту
        return Response(content, status=response.status_code, headers=headers)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error during proxying: {e}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083)
