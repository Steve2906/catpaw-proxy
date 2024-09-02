import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy(path):
    """Проксирование запросов."""
    target_url = request.url.replace(request.host_url, "")
    if not target_url:
        return "URL is required", 400

    try:
        # Выполнение проксируемого запроса к целевому URL
        response = requests.get(target_url)

        # Возвращение контента ответа с сохранением статуса и типа содержимого
        return Response(response.content, status=response.status_code, content_type=response.headers.get('Content-Type'))
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8083)
