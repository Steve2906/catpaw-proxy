from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy/')
def proxy():
    target_url = request.args.get('url')
    
    if not target_url:
        return "URL is required", 400
    
    try:
        # Проксируем запрос на целевой URL
        response = requests.get(target_url)
        headers = dict(response.headers)
        
        # Удаляем заголовки, которые могут помешать отображению и работе контента в iframe
        headers.pop('X-Frame-Options', None)
        headers.pop('Content-Security-Policy', None)
        headers.pop('Access-Control-Allow-Origin', None)
        headers.pop('Strict-Transport-Security', None)
        
        # Дополнительно можем добавить заголовок для разрешения CORS, если необходимо
        headers['Access-Control-Allow-Origin'] = '*'
        
        # Возвращаем проксированный ответ
        return Response(response.content, headers=headers, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083)
