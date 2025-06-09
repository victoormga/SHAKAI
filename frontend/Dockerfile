# 1. Imagen base Node ligera
FROM node:18-alpine

# 2. Directorio de trabajo
WORKDIR /app

# 3. Copiar package.json e instalar dependencias
COPY package.json package-lock.json* ./
RUN npm install

# 4. Copiar el resto del código
COPY . .

# 5. Construir la app para producción (genera dist/)
RUN npm run build

# 6. Instalar servidor estático y exponer puerto
RUN npm install -g http-server
EXPOSE 5173

# 7. Servir la carpeta dist
CMD ["http-server", "dist", "-p", "5173", "-c-1"]