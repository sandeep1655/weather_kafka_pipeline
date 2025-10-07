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

## System Architecture

```mermaid
flowchart TD

subgraph Local_Docker_Network ["Local Docker Network (Bridge)"]
    A[Flask App Container] -->|Publishes weather data| B[Kafka Broker Container]
    B --> C[Kafka Consumer Container]
    C -->|Writes batched JSON files| D[Local Volume: data/bronze]
    D -->|Watched by uploader.py| E[Snowflake Cloud Warehouse]
end

E --> F[Power BI Desktop / Service]

subgraph External_Services ["External APIs"]
    G[OpenWeather API]
end

G -->|Fetch city weather data| A

classDef docker fill:#f8f9fa,stroke:#333,stroke-width:1px;
classDef external fill:#eaf4ff,stroke:#333,stroke-width:1px;
classDef cloud fill:#f0fff4,stroke:#333,stroke-width:1px;
class A,B,C,D docker;
class E cloud;
class F,G external;


