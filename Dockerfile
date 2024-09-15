# Build phase for testing and development
FROM python:3.11-slim AS builder
WORKDIR /app

# Install essential dependencies
RUN apt-get update && apt-get install -y gcc g++ make libssl-dev

COPY requirementsL.txt requirements-api.txt ./
RUN pip install --no-cache-dir -r requirementsL.txt

# Essential files and test folder to run tests
COPY Makefile ./
COPY challenge/api.py challenge/
COPY challenge/model.py challenge/
COPY challenge/trained_model_with_metadata.joblib challenge/
COPY tests/ tests/
COPY data/data.csv data/

RUN make model-test && make api-test

# Final phase: clean image for production
FROM python:3.11-slim
WORKDIR /app

# Instalar dependencias mínimas necesarias para producción
RUN apt-get update && apt-get install -y gcc g++ make libssl-dev

# Copiar solo los archivos necesarios desde la fase builder
COPY --from=builder /app/challenge/api.py /app/challenge/
COPY --from=builder /app/challenge/model.py /app/challenge/
COPY --from=builder /app/challenge/trained_model_with_metadata.joblib /app/challenge/

# Instalar solo las dependencias de producción
COPY requirements-api.txt ./
RUN pip install --no-cache-dir -r requirements-api.txt

EXPOSE 8080
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
