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
