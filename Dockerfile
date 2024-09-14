FROM python:3.11-slim
WORKDIR /app

COPY requirementsD.txt ./
RUN pip install --no-cache-dir -r requirementsD.txt

# File essentials
COPY challenge/api.py challenge/
COPY challenge/model.py challenge/
COPY challenge/trained_model_with_metadata.joblib challenge/

# Incluir la carpeta de tests (para las pruebas de stress y otras)
COPY tests/ tests/

EXPOSE 8000
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8000"]
