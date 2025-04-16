from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NEWS_API_KEY = 'pub_808730828b8d9584c94e98325e4430b236db8'

@app.route('/retrieval', methods=['POST'])
def get_news():
    # Получаем вопрос от агента (можно использовать для фильтрации)
    user_question = request.json.get("query", "")

    # Запрашиваем новости
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWS_API_KEY,
        "language": "ru",
        "q": user_question,
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for article in data.get("results", [])[:5]:  # Ограничим до 5 новостей
        title = article.get("title", "Без заголовка")
        description = article.get("description", "")
        results.append(f"{title}: {description}")

    return jsonify({
        "answer": "\n\n".join(results)
    })

@app.route('/', methods=['GET'])
def home():
    return '✅ Сервер работает. Ожидается POST-запрос на /retrieval', 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
