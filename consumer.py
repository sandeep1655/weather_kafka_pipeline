# consumer_time_window.py
from kafka import KafkaConsumer
import json, os, time
from datetime import datetime

TOPIC = "weather_topic"
OUT_DIR = os.path.join("data", "bronze")
os.makedirs(OUT_DIR, exist_ok=True)

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id=None
)

print("📡 Listening and writing a JSON file every 60s...")

window_secs = 60
batch = []
window_start = time.time()

def write_file(records):
    if not records:
        return None
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    fname = f"weather_{ts}.json"  # one file per minute
    fpath = os.path.join(OUT_DIR, fname)
    with open(fpath, "w") as f:
        json.dump(records, f, indent=2)
    print(f"💾 Wrote {len(records)} records to {fpath}")
    return fpath

while True:
    msg = next(consumer)
    batch.append(msg.value)

    if time.time() - window_start >= window_secs:
        write_file(batch)
        batch.clear()
        window_start = time.time()




