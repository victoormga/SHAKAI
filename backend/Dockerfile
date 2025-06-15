# 1. Imagen base Python
FROM python:3.11-slim

# 2. Evitar bytecode y buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Instalación de dependencias de sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       default-libmysqlclient-dev \
       netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 4. Directorio de trabajo
WORKDIR /app

# 5. Copiar e instalar dependencias Python
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \

# 6. Copiar el resto del código
COPY . .

# 7. Exponer puerto
EXPOSE 8000

# 8. Variables de entorno (deben coincidir con settings.py: DB_NAME, DB_USER...)
ENV DB_NAME=mydb
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
ENV DB_HOST=db
ENV DB_PORT=3306

# 9. Migrar y arrancar
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]