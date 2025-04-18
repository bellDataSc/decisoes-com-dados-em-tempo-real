# decisoes-com-dados-em-tempo-real

decisoes-com-dados-em-tempo-real/
├── README.md
├── notebooks/
│   └── pipeline_spark_streaming.ipynb
├── data/
│   └── simulados/         # arquivos CSV para simular streaming
├── src/
│   ├── producer.py        # simula envio de dados contínuos (pasta sendo alimentada ou socket)
│   └── spark_pipeline.py  # script principal com Spark Structured Streaming
├── dashboard/
│   └── app_streamlit.py   # dashboard simples de visualização
├── requirements.txt
├── docker-compose.yml     # se quiser containerizar o Spark ou simular Kafka
└── .gitignore
