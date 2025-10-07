import os, time
import snowflake.connector
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Read Snowflake creds from env vars (set these in .env or docker-compose.yml)
SF_USER = os.getenv("SNOWFLAKE_USER")
SF_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SF_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")      # e.g. abcd-xy12345
SF_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")  # e.g. COMPUTE_WH
SF_DATABASE = os.getenv("SNOWFLAKE_DATABASE")    # e.g. MYDB
SF_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")        # e.g. PUBLIC

WATCH_DIR = os.path.join("data", "bronze")       # where consumer writes files

conn = snowflake.connector.connect(
    user=SF_USER,
    password=SF_PASSWORD,
    account=SF_ACCOUNT,
    warehouse=SF_WAREHOUSE,
    database=SF_DATABASE,
    schema=SF_SCHEMA,
)
cur = conn.cursor()

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith(".json"):
            return

        file_name = os.path.basename(event.src_path)

        # ✅ Only process files created by consumer_time_window.py
        if not file_name.startswith("weather_window_"):
            print(f"⏭️ Skipping non-window file: {file_name}")
            return

        local_path = os.path.abspath(event.src_path)
        file_uri = "file://" + local_path.replace("\\", "/")

        print(f"📂 New file detected: {local_path}")

        # 1) PUT to stage (no compression so name stays the same)
        cur.execute(f"PUT '{file_uri}' @MY_STAGE AUTO_COMPRESS=FALSE")
        print(f"✅ Staged: @MY_STAGE/{file_name}")

        # 2) COPY into the structured table, then purge staged copy
        cur.execute(f"""
            COPY INTO WEATHER_DATA_JSON
            FROM @MY_STAGE/{file_name}
            FILE_FORMAT=(FORMAT_NAME=MY_JSON_FORMAT)
            MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE
            ON_ERROR='CONTINUE'
            PURGE=TRUE
        """)
        print(f"💾 Loaded into WEATHER_DATA_JSON and purged staged file\n")

def main():
    os.makedirs(WATCH_DIR, exist_ok=True)
    print(f"👀 Watching: {os.path.abspath(WATCH_DIR)}")
    observer = Observer()
    observer.schedule(NewFileHandler(), WATCH_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
