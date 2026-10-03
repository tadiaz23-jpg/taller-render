# Dockerfile optimizado para producción en Render y GitHub Container Registry (GHCR)
FROM python:3.12-slim

# Evitar escritura de archivos .pyc y buffer de salida de python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema si fueran requeridas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación
COPY . .

# Ejecutar la suite de pruebas durante la construcción de la imagen (Red de seguridad en el Build)
RUN pytest -v

# Exponer el puerto por defecto de la aplicación
EXPOSE 5000

# Endpoint de comprobación de salud del contenedor
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Comando de inicio con Gunicorn para producción
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
