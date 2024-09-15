# Resolución de desafío para Ingeniero de Software (ML y LLMs)

## Resumen
He completado el desafío para Ingeniero de Software (ML y LLMs), que consistió en operacionalizar un modelo de predicción de retrasos de vuelos y desplegarlo en una API utilizando FastAPI y GCP. A continuación, detallo los pasos seguidos para completar el desafío.

---

## 1.- Transcripción y ajuste del modelo
Adapté el código de exploration.ipynb al archivo model.py, corrigiendo errores y asegurando su funcionalidad. Probé los 6 modelos propuestos por el científico de datos y evalúe las métricas (precisión, recall y f1-score), los modelos con mejor desempeño fueron:

1. *Logistic Regression with Feature Importance and with Balance*
2. *XGBoost with Feature Importance and with Balance*

Ambos modelos arrojaron resultados muy similares en cuanto a las métricas de evaluación. Sin embargo, elegí el modelo de *Regresión Logística* por su simplicidad, interpretabilidad y menor costo computacional, especialmente relevante en entornos de producción donde la eficiencia es clave.

---

## 2.- Desarrollo de model.py
En model.py, desarrollé la clase DelayModel con tres métodos principales:

- preprocess: Procesa los datos de vuelo, calcula la diferencia en minutos entre la salida y llegada, marca los vuelos retrasados y selecciona las 10 características más importantes para el modelo.
- fit: Entrena el modelo de regresión logística con los datos preprocesados.
- predict: Realiza predicciones sobre los vuelos, devolviendo si habrá retraso o no.

El código fue probado y pasó las pruebas ejecutando make model-test.

---

## 3.- Entrenamiento del modelo con train_model.py
En train_model.py, desarrollé el flujo de entrenamiento del modelo. Este script carga los datos desde data.csv, realiza el preprocesamiento de las características usando la clase DelayModel y entrena el modelo de regresión logística. Después de entrenar el modelo, guardo el modelo, el preprocesador y las características en el archivo trained_model_with_metadata.joblib, para su posterior uso en la API.

---

## 4.- Implementación de la API con FastAPI
Implementé la API utilizando FastAPI en el archivo api.py. La API realiza lo siguiente:

- *Carga el modelo entrenado*: Extrae el modelo, el preprocesador y las características almacenadas en el archivo trained_model_with_metadata.joblib.
- *Validación de datos de entrada*: Asegura que las entradas del usuario (como aerolínea, tipo de vuelo, mes) sean válidas antes de realizar las predicciones.
- *Endpoints*:
  - /predict: Recibe solicitudes POST con datos de vuelo, aplica el preprocesador y devuelve la predicción de retraso.
  - /health: Proporciona el estado de la API.

Las pruebas de la API fueron exitosas al ejecutar make api-test.

---

## 5.- Despliegue en GCP
Después de superar las pruebas de modelo y API, creé una imagen de Docker optimizada para producción, utilizando un Dockerfile con dos fases. La primera fase para pruebas y desarrollo, donde instalé las dependencias completas y ejecuté los tests con make model-test y make api-test. La segunda fase es una imagen limpia para producción, donde copié solo los archivos necesarios y las dependencias mínimas desde un archivo reducido (requirements-api.txt). Finalmente, desplegué la API en los servidores de GCP, seleccionando la región de Chile debido a su buena latencia y el rendimiento en las pruebas iniciales, además aquí está la sede principal de LATAM.

Realicé pruebas de estrés ejecutando make stress-test, y los resultados fueron satisfactorios: el 99% de las solicitudes fueron procesadas en menos de 760 ms y manejo bien el volumen de solicitudes sin errores ni caídas de servicio. A pesar de esto, existen oportunidades para optimizar aún más el rendimiento.

*Enlace a la API*: [https://prediction-api-333225756069.southamerica-west1.run.app]

---

## 6.- Implementación de CI/CD
Implementé los pipelines de CI/CD utilizando GitHub Actions. En la carpeta .github/workflows, configuré los archivos ci.yml y cd.yml siguiendo las mejores prácticas. Sin embargo, me encontré con problemas de compatibilidad relacionados con versiones obsoletas de Node.js (Node16), lo que impidió el éxito de las pruebas en CI/CD. Debido a limitaciones de tiempo, no investigué la solución en profundidad, pero es un área a mejorar.

---

## Conclusión
Completé con éxito las pruebas de modelo, API, estrés y el despliegue en GCP. Aunque el pipeline de CI/CD quedó pendiente por problemas de compatibilidad con Node.js, el modelo y la API están funcionales y listos para producción.
