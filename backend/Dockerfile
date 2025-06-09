# 1. Imagen base Python
FROM python:3.11-slim

# 2. Variables de entorno para bytecode y logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo
WORKDIR /app

# 4. Dependencias del sistema para MySQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar e instalar dependencias Python
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 6. Copiar el resto del código
COPY . .

# 7. Exponer puerto de Django
EXPOSE 8000

# 8. Variables de entorno para la base de datos (coincidir con docker-compose)
ENV DATABASE_NAME=mydb
ENV DATABASE_USER=myuser
ENV DATABASE_PASSWORD=mypassword
ENV DATABASE_HOST=db
ENV DATABASE_PORT=3306

# 9. Comando por defecto: migrar y arrancar
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]