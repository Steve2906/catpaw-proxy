from flask import Flask, request, Response
import requests
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@app.route('/proxy')
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

        # Логирование успешного запроса
        app.logger.info(f"Successfully proxied request to: {target_url}")
        
        # Возвращение оригинального контента обратно клиенту
        return Response(response.content, status=response.status_code, content_type=response.headers.get('Content-Type'))
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error during proxying: {e}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083)
