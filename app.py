from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

NEWS_API_KEY = 'pub_808730828b8d9584c94e98325e4430b236db8'

@app.route('/retrieval', methods=['POST'])
def get_news():
    data = request.json
    user_question = data.get("query", "")
    knowledge_id = data.get("knowledge_base_id", "")
    
    if knowledge_id != "news-db":
        return jsonify({"answer": "Unknown knowledge base."}), 400
    
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWS_API_KEY,
        "language": "ru",
        "q": user_question,
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for article in data.get("results", [])[:10]:
        title = article.get("title", "Без заголовка")
        description = article.get("description", "")
        results.append(f"{title}: {description}")

    if not results:
        return jsonify({
            "answer": "Не удалось найти новости по вашему запросу."
        })

    return jsonify({
        "answer": "\n\n".join(results)
    })

@app.route('/', methods=['GET'])
def home():
    return '✅ Сервер работает. Ожидается POST-запрос на /retrieval', 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
