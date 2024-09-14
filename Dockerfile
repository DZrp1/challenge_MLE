FROM python:3.11-slim
WORKDIR /app

# Install essential dependencies to compile packages like pandas
RUN apt-get update && apt-get install -y gcc g++ make libssl-dev

COPY requirementsL.txt ./
RUN pip install --no-cache-dir -r requirementsL.txt

# File essentials
COPY challenge/api.py challenge/
COPY challenge/model.py challenge/
COPY challenge/trained_model_with_metadata.joblib challenge/

# Incluir la carpeta de tests
COPY tests/ tests/

EXPOSE 8000
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
