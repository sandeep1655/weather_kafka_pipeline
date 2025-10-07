from flask import Flask, render_template, request
import requests, os, json
from kafka import KafkaProducer

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY", "your_api_key")  # replace with your real key

# Kafka bootstrap server (works both locally and in Docker)
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"]
            }
            # ✅ Send to Kafka
            producer.send("weather_topic", weather_data)
            producer.flush()
            print("✅ Sent to Kafka:", weather_data)
        else:
            weather_data = {"error": "City not found!"}
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)  # 0.0.0.0 so it works in Docker

