# weather_kafka_pipeline
# 🌦 End-to-End Weather Data Engineering Pipeline  

A **modern data engineering pipeline** that ingests real-time weather data using a Flask web app, streams it through Apache Kafka, stores it as JSON files (bronze layer), uploads it to **Snowflake**, and visualizes insights in **Power BI**.  
Everything runs seamlessly in **Docker** containers for easy setup and reproducibility.  

---

## 🧠 Project Overview  

This project demonstrates the **entire lifecycle of a data pipeline** — from ingestion to visualization — simulating a real-world streaming data workflow used in enterprise analytics.  

- 🌐 **Flask** → serves as the API ingestion layer to fetch live weather data.  
- ⚙️ **Apache Kafka** → acts as a distributed event-streaming platform to transmit data in real time.  
- 💾 **Consumers** → listen to Kafka topics and store JSON records locally (bronze layer).  
- ☁️ **Snowflake** → stores structured data for analytical processing.  
- 📊 **Power BI** → visualizes the data in interactive dashboards.  

---

## 🏗️ System Architecture  

```mermaid
flowchart TD
    A[User Input: Flask App] -->|Fetch Weather API| B[OpenWeather API]
    B -->|Send JSON| C[Kafka Producer]
    C -->|Push to Topic| D[Kafka Broker]
    D -->|Consume Messages| E[Kafka Consumer]
    E -->|Write JSON Files| F[data/bronze/ Folder]
    F -->|Watchdog + Snowflake Connector| G[Snowflake Stage]
    G -->|COPY INTO Command| H[Snowflake Weather Table]
    H -->|Live Connection| I[Power BI Dashboard]

