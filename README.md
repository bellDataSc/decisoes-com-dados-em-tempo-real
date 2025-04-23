# Real-Time Data-Driven Decisions

This project simulates a real-time data pipeline using **Apache Spark Structured Streaming** and visualizes the processed data in a live dashboard using **Streamlit**.  
It is part of my specialization at **Mackenzie University** in the course *"Data-Driven Decision Making in Real Time"*.

The goal is to demonstrate how decisions can be guided by data — structured or unstructured — through an end-to-end pipeline from data ingestion to real-time decision support.



---

## 🚀 Technologies Used

- **Python 3.10+**
- **Apache Spark** (Structured Streaming)
- **Streamlit**
- **Pandas**
- **Faker** (for generating realistic fake data)
- **Docker** (optional: containerizing Spark or simulating Kafka)
- **Jupyter Notebook** (for exploratory analysis)

---

## 📁 Project Structure

The project is organized as follows:

```bash
real-time-data-driven-decisions/
├── README.md                     # This file
├── notebooks/
│   └── pipeline_spark_streaming.ipynb   # Jupyter Notebook for exploratory setup
├── data/
│   └── simulated/                # CSV files simulating the stream
├── src/
│   ├── producer.py              # Script to simulate continuous data input
│   └── spark_pipeline.py        # Spark Structured Streaming main script
├── dashboard/
│   └── app_streamlit.py         # Streamlit dashboard for live data visualization
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Optional: to containerize Spark or simulate Kafka
└── .gitignore                   # Files and folders to ignore in version control


