from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NEWS_API_KEY = 'ТВОЙ_API_КЛЮЧ'

@app.route('/news', methods=['POST'])
def get_news():
    data = request.get_json()
    user_query = data.get("query", "")
    
    # Не используем knowledge_id, просто игнорируем
    print(f"[INFO] Запрос от Dify: {user_query}")
    
    # Запрос к внешнему API
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWS_API_KEY,
        "language": "ru",
        "q": user_query,
        "category": "top,world,technology,health,entertainment,business"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"answer": f"Ошибка получения новостей: {response.status_code}"}), 500

    data = response.json()
    results = []
    for article in data.get("results", [])[:20]:  # до 20 новостей
        title = article.get("title", "Без заголовка")
        description = article.get("description", "")
        results.append(f"{title}: {description}")

    if not results:
        return jsonify({"answer": "Новости по запросу не найдены."})

    return jsonify({
        "answer": "\n\n".join(results)
    })

@app.route('/', methods=['GET'])
def home():
    return '✅ Сервер работает. Используй POST /news для получения новостей.'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
