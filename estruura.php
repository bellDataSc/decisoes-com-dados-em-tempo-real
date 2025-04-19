decisoes-com-dados-em-tempo-real/
├── README.md
├── notebooks/
│   └── pipeline_spark_streaming.ipynb
├── data/
│   └── simulados/         # deixe os CSV aqui
├── src/
│   ├── producer.py        # script para gerar dados simulados
│   └── spark_pipeline.py  # pipeline com Spark Structured Streaming
├── dashboard/
│   └── app_streamlit.py   # dashboard em tempo real
├── requirements.txt
├── docker-compose.yml     # opcional, para ambiente containerizado
└── .gitignore
