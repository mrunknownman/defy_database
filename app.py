from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NEWS_API_KEY = 'pub_808730828b8d9584c94e98325e4430b236db8'
MY_SECRET_API_KEY = 'apikey'  # этот будет проверяться из request.json["api_key"]

@app.route('/retrieval', methods=['POST'])
def get_news():
    data = request.json or {}
    user_key = data.get("api_key", "")

    if user_key != MY_SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    user_query = data.get("query", "")
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWS_API_KEY,
        "language": "ru",
        "q": user_query,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"answer": f"Ошибка получения новостей: {response.status_code}"}), 422

    news_data = response.json()
    results = []
    for article in news_data.get("results", [])[:10]:
        title = article.get("title", "Без заголовка")
        description = article.get("description", "")
        link = article.get("link", "")
        results.append(f"📰 {title}\n{description}\n🔗 {link}")

    return jsonify({
        "answer": "\n\n".join(results)
    })

@app.route('/', methods=['GET'])
def home():
    return "✅ Сервер работает. Эндпоинт: /retrieval (POST)", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
