from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import spacy
from textblob import TextBlob
import openai
import os

app = Flask(__name__)
CORS(app)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.chatbot_db
chats = db.chats

# ✅ OpenAI GPT API key setup (store your API key as an environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Sentiment Analysis using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"

# ✅ Generate reply using GPT
def generate_gpt_reply(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive mental health chatbot."},
                {"role": "user", "content": message}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "I'm having trouble generating a response. Please try again later."

# ✅ Chat endpoint with sentiment + GPT
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").lower()
    sentiment = analyze_sentiment(msg)
    gpt_reply = generate_gpt_reply(msg)

    # Save to DB
    chats.insert_one({
        "user": msg,
        "bot": gpt_reply,
        "sentiment": sentiment,
        "timestamp": datetime.datetime.utcnow()
    })

    return jsonify({"response": gpt_reply, "sentiment": sentiment})

# ✅ Dashboard data endpoint (sentiment counts)
@app.route("/dashboard-data", methods=["GET"])
def dashboard_data():
    pipeline = [
        {"$group": {
            "_id": "$sentiment",
            "count": {"$sum": 1}
        }}
    ]
    data = list(chats.aggregate(pipeline))
    return jsonify(data)

# ✅ Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5002)
