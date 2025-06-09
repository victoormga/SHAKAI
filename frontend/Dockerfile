# 1. Imagen Node ligera
FROM node:18-alpine

# 2. Directorio de trabajo
WORKDIR /app

# 3. Copiar y instalar deps
COPY package.json package-lock.json* ./
RUN npm install

# 4. Copiar código y generar build
COPY . .
RUN npm run build

# 5. Instalar http-server y exponer puerto de producción
RUN npm install -g http-server
EXPOSE 5175

# 6. Servir carpeta dist sin cache (-c-1)
CMD ["http-server", "dist", "-p", "5175", "-c-1"]